#include "mainwindow.h"
#include <QGraphicsTextItem>
#include <QHBoxLayout>
#include <QLabel>
#include <QMessageBox>
#include <QVBoxLayout>

const int k1000=1000;
const int k5=5;
const int k10=10;
const int k2=2;
const int k4=4;
const int k30=30;
const int k20=20;
const int k255=255;
const int k50=50;
const int k400=400;
const int k600=600;
const int k800=800;
const int k1=1;
const int k8=8;
const int k100=100;
const int k10000=10000;
const int k200=200;
const int k300=300;
const int k310=310;
const int k90=90;
const int k290=290;
const int k490=490;
const int k25=25;

MainWindow::MainWindow(QWidget* parent) : QMainWindow(parent) {
    setupUI();
    currentMove_ = 0;
    towers_.resize(3);
    animationSpeed_ = k1000;
    animationTimer_ = new QTimer(this);
    connect(animationTimer_, &QTimer::timeout, this,
            &MainWindow::performAutoStep);
}

MainWindow::~MainWindow() {}

void MainWindow::setupUI() {
    QWidget* central_widget = new QWidget(this);
    QVBoxLayout* main_layout = new QVBoxLayout(central_widget);

    QHBoxLayout* control_layout = new QHBoxLayout();

    QLabel* label = new QLabel("Количество колец:", this);
    ringsCountEdit_ = new QLineEdit("3", this);
    ringsCountEdit_->setMaximumWidth(k50);

    QLabel* speed_label = new QLabel("Скорость (мс):", this);
    speedEdit_ = new QLineEdit("1000", this);
    speedEdit_->setMaximumWidth(k50);

    initializeButton_ = new QPushButton("Инициализировать", this);
    connect(initializeButton_, &QPushButton::clicked, this,
            &MainWindow::initializeTower);

    startButton_ = new QPushButton("Старт", this);
    startButton_->setEnabled(false);
    connect(startButton_, &QPushButton::clicked, this,
            &MainWindow::startAnimation);

    control_layout->addWidget(label);
    control_layout->addWidget(ringsCountEdit_);
    control_layout->addWidget(speed_label);
    control_layout->addWidget(speedEdit_);
    control_layout->addWidget(initializeButton_);
    control_layout->addWidget(startButton_);
    moveCounterLabel_ = new QLabel("Ходов: 0", this);
    control_layout->addWidget(moveCounterLabel_);

    scene_ = new QGraphicsScene(this);
    graphicsView_ = new QGraphicsView(scene_, this);
    graphicsView_->setRenderHint(QPainter::Antialiasing);
    graphicsView_->setSceneRect(0, 0, k600, k400);

    main_layout->addLayout(control_layout);
    main_layout->addWidget(graphicsView_);

    setCentralWidget(central_widget);
    resize(k800, k600);
    setWindowTitle("Ханойская башня с анимацией");
}

void MainWindow::initializeTower() {
    bool ok;
    int rings_count = ringsCountEdit_->text().toInt(&ok);


    if (!ok || rings_count < k1 || rings_count > k8) {
        QMessageBox::warning(this, "Ошибка", "Введите число от 1 до 8");
        return;
    }

    animationSpeed_= speedEdit_->text().toInt(&ok);


    // Проверка скорости анимации
    bool ok_speed;
    int input_speed = speedEdit_->text().toInt(&ok_speed);

    // Если ввод не число или вне диапазона


    if (!ok_speed || input_speed < k100 || input_speed > k10000) {
        QMessageBox::warning(
            this, "Ошибка",
            "Скорость должна быть целым числом от 100 до 10000 мс");
        speedEdit_->setText("1000");	 // сброс на стандартное значение
        animationSpeed_ = k1000;
    } else {
        animationSpeed_ = input_speed;
    }


    initializeTowers(rings_count);
    moves_ = hanoiSolver_.Hanoi(rings_count, 1, 3);
    currentMove_ = 0;
    moveCount_ = 0;
    moveCounterLabel_->setText("Ходов: 0");

    startButton_->setEnabled(true);
}

void MainWindow::startAnimation() {
    startButton_->setEnabled(false);
    initializeButton_->setEnabled(false);
    animationTimer_->start(animationSpeed_);
}

void MainWindow::performAutoStep() {
    if (currentMove_ >= moves_.size()) {
        animationTimer_->stop();
        QMessageBox::information(this, "Готово", "Все кольца перемещены!");
        initializeButton_->setEnabled(true);
        return;
    }

    QPair<int, int> move = moves_[currentMove_];
    int from = move.first - 1;
    int to = move.second - 1;

    if (!towers_[from].isEmpty()) {
        int ring_value = towers_[from].last();
        int ring_index = ringsCount_ - ring_value;	 // Получаем индекс кольца
        animateRing(ring_index, from, to);
    }

    currentMove_++;
    moveCount_++;
    moveCounterLabel_->setText(QString("Ходов: %1").arg(moveCount_));
}

void MainWindow::animateRing(int ringIndex, int fromTower, int toTower) {
    int ring_value = ringsCount_ - ringIndex;
    towers_[fromTower].removeLast();

    RingItem* ring = ringItems_[ringIndex];

    int base_y = k300;
    int lift_height = k200;

    QPointF start_pos = ring->pos();
    QPointF lift_pos = QPointF(start_pos.x(), start_pos.y() - lift_height);

    int width = ringWidths_[ringIndex];
    int target_x = k100 + toTower * k200 - width / 2;

    int stack_height = towers_[toTower].size();
    int target_y = base_y - (stack_height + 1) * k25;
    QPointF above_target_pos = QPointF(target_x, lift_pos.y());
    QPointF end_pos = QPointF(target_x, target_y);

    towers_[toTower].append(ring_value);

    QSequentialAnimationGroup* animation_group =
        new QSequentialAnimationGroup(this);

    QPropertyAnimation* lift_animation = new QPropertyAnimation(ring, "pos");
    lift_animation->setDuration(animationSpeed_ / 3);
    lift_animation->setStartValue(start_pos);
    lift_animation->setEndValue(lift_pos);

    QPropertyAnimation* move_animation = new QPropertyAnimation(ring, "pos");
    move_animation->setDuration(animationSpeed_ / 3);
    move_animation->setStartValue(lift_pos);
    move_animation->setEndValue(above_target_pos);

    QPropertyAnimation* drop_animation = new QPropertyAnimation(ring, "pos");
    drop_animation->setDuration(animationSpeed_ / 3);
    drop_animation->setStartValue(above_target_pos);
    drop_animation->setEndValue(end_pos);

    animation_group->addAnimation(lift_animation);
    animation_group->addAnimation(move_animation);
    animation_group->addAnimation(drop_animation);

    connect(animation_group, &QAbstractAnimation::finished, this,
            &MainWindow::onAnimationFinished);
    animation_group->start(QAbstractAnimation::DeleteWhenStopped);
}

void MainWindow::onAnimationFinished() {}

void MainWindow::initializeTowers(int count) {
    ringsCount_ = count;
    towers_.clear();
    towers_.resize(3);
    ringItems_.clear();
    ringWidths_.clear();
    scene_->clear();


    for (int i = 0; i < count; ++i) {
        int ring_value = count - i;
        towers_[0].append(ring_value);
    }

    int base_y = k300;


    for (int i = 0; i < 3; ++i) {
        scene_->addRect(k100 + i * k200 - k5, base_y, k10, k10, QPen(),
                       QBrush(Qt::black));
        scene_->addRect(k100 + i * k200 - k2, base_y - k200, k4, k200, QPen(),
                       QBrush(Qt::black));
    }


    for (int i = 0; i < count; ++i) {
        int ring_value = i + 1;
        int ring_index = count - ring_value;

        int width = k30 + (count - ring_value + 1) * k20;

        int x = k100 - width / k2;
        int y = base_y - (ring_value) * k25;

        RingItem* ring = new RingItem();
        ring->setRect(0, 0, width, k20);
        ring->setPos(x, y);
        ring->setBrush(QColor::fromHsv(ring_index * k30, k255, k200));
        ring->setPen(QPen(Qt::black));


        scene_->addItem(ring);
        ringItems_.append(ring);
        ringWidths_.append(width);
    }

    scene_->addText("A")->setPos(k90, k310);
    scene_->addText("B")->setPos(k290, k310);
    scene_->addText("C")->setPos(k490, k310);
}

#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QGraphicsRectItem>
#include <QGraphicsScene>
#include <QGraphicsView>
#include <QLabel>
#include <QLineEdit>
#include <QMainWindow>
#include <QObject>
#include <QPropertyAnimation>
#include <QPushButton>
#include <QSequentialAnimationGroup>
#include <QTimer>
#include "function.h"

class RingItem : public QObject, public QGraphicsRectItem {
    Q_OBJECT
    Q_PROPERTY(QPointF pos READ pos WRITE setPos)
public:
    using QGraphicsRectItem::QGraphicsRectItem;
};

class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    MainWindow(QWidget* parent = nullptr);
    ~MainWindow();

private slots:
    void initializeTower();
    void startAnimation();
    void performAutoStep();
    void onAnimationFinished();

private:
    void setupUI();
    void drawTowers();
    void initializeTowers(int rings);
    void animateRing(int ringNumber, int fromTower, int toTower);

    // Виджеты
    QGraphicsScene* scene_;
    QGraphicsView* graphicsView_;
    QLineEdit* ringsCountEdit_;
    QLineEdit* speedEdit_;
    QPushButton* initializeButton_;
    QPushButton* startButton_;
    QLabel* moveCounterLabel_;

    // Логика
    Function hanoiSolver_;
    QVector<QPair<int, int>> moves_;
    int currentMove_;
    int moveCount_;
    QVector<QVector<int>> towers_;
    QVector<QRect> rings_;
    QVector<RingItem*> ringItems_;
    QVector<int> ringWidths_;
    QTimer* animationTimer_;
    int animationSpeed_;
    int ringsCount_;
};

#endif	// MAINWINDOW_H

using _453503_Khalamau_Lab1.Interfaces;

namespace _453503_Khalamau_Lab1.Collections
{
    public class MyCustomCollection<T> : ICustomCollection<T>
    {
        private class Node
        {
            public T Value { get; set; }

            public Node Next { get; set; }

            public Node(T value)
            {
                Value = value;
                Next = null;
            }
        }

        private Node head;
        private Node tail;
        private Node cursor;
        private int count;

        public MyCustomCollection()
        {
            head = null;
            tail = null;
            cursor = null;
            count = 0;
        }

        public T this[int index]
        {
            get
            {
                if (index < 0 || index >= count)
                    throw new IndexOutOfRangeException("Index can not be negative or bigger than collection size");

                Node current = head;
                for (int i = 0; i < index; i++)
                {
                    current = current.Next;
                }
                return current.Value;
            }
            set
            {
                if (index < 0 || index >= count)
                    throw new IndexOutOfRangeException("Index can not be negative or bigger than collection size");

                Node current = head;
                for (int i = 0; i < index; i++)
                {
                    current = current.Next;
                }
                current.Value = value;
            }
        }

        public void Reset()
        {
            cursor = head;
        }

        public void Next()
        {
            if (cursor != null)
            {
                cursor = cursor.Next;
            }
        }
        public T Current()
        {
            if (cursor == null)
            {
                throw new InvalidOperationException("Cursor is not pointing to any element.");
            }
            return cursor.Value;
        }

        public int Count 
        {
            get => count;
        }

        public void Add(T item)
        {
            Node newNode = new Node(item);
            if (head == null)
            {
                head = newNode;
                tail = newNode;
            }
            else
            {
                tail.Next = newNode;
                tail = newNode;
            }

            count++;
            if (cursor == null)
            {
                cursor = head;
            }
        }

        public void Remove(T item)
        {
            if (head==null)
            {
                return;
            }

            if (EqualityComparer<T>.Default.Equals(head.Value,item))
            {
                head = head.Next;
                count--;
                if (head==null)
                {
                    tail = null;
                }
                if (cursor == null || EqualityComparer<T>.Default.Equals(cursor.Value, item))
                {
                    cursor = head;
                }
                return;
            }

            Node current = head;
            Node previous = null;

            while (current != null && !EqualityComparer<T>.Default.Equals(current.Value, item))
            {
                previous = current;
                current = current.Next;
            }

            if (current != null)
            {
                previous.Next = current.Next;
                if (current==tail)
                {
                    tail = previous;
                }
                if (current==cursor)
                {
                    cursor = current.Next;
                }
                count--;
            }
        }

        public T RemoveCurrent()
        {
            if (cursor == null)
                throw new InvalidOperationException("Cursor is not pointing to any element.");

            T value = cursor.Value;

            if (cursor == head)
            {
                head = head.Next;
                cursor = head;
                if (head == null)
                { 
                    tail = null;
                }
                   
                count--;
                return value;
            }

            Node current = head;
            Node previous = null;
            while (current != null && current != cursor)
            {
                previous = current;
                current = current.Next;
            }

            if (current == null)
                throw new InvalidOperationException("Cursor is invalid.");

            previous.Next = cursor.Next;

            if (cursor == tail)
            {
                tail = previous;
            }
                
            cursor = cursor.Next;
            count--;

            return value;
        }

        public bool HasCurrent => cursor != null;

    }
}

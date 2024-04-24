class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.head.next = self.head  # 원형 구조를 만들기 위해 자신을 가리키도록 함
        else:
            current = self.head
            while current.next != self.head:  # 시작 노드로 돌아올 때까지 반복
                current = current.next
            current.next = new_node
            new_node.next = self.head  # 새 노드의 다음 노드를 첫 노드로 설정하여 원을 완성

    def print_list(self):
        current = self.head
        if self.head:
            while True:
                print(current.data, end=' ')
                current = current.next
                if current == self.head:
                    break
            print()  # 줄바꿈을 위한 print

# 사용 예제
cllist = CircularLinkedList()
cllist.append(1)
cllist.append(2)
cllist.append(3)

cllist.print_list()  # 1 2 3 출력
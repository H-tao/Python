from abc import abstractmethod

class A:
    def get_info(self):
        self._get()

    @abstractmethod
    def _get(self):
        pass

class B(A):
    def _get(self):
        print('B _get')

class C(A):
    def _get(self):
        print('C _get')

if __name__ == '__main__':
    b = B()
    b.get_info()
    c = C()
    c.get_info()

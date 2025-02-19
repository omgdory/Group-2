//By: Abdulrahman ALharbi 
// i tried to make very complex code for chatGPT 
// let's see my c++ skills! 
// im thinking of 
    //operator overloading
    //inheritance (overriding)
    //and of course pointers......
#include <iostream>

class Base {
public:
    virtual void display() const { 
        std::cout << "Base class display function\n"; 
    }
    Base operator+(const Base& other) {
        std::cout << "Base + operator overloaded\n";
        return Base();
    }
    virtual ~Base() { std::cout << "Base Destructor\n"; }
};

class Derived : public Base {
private:
    int* data; 
public:
    Derived(int val) {
        data = new int(val);
        std::cout << "Derived Constructor: Allocated memory\n";
    }
    Derived(const Derived& other) {
        data = new int(*(other.data));
        std::cout << "Derived Copy Constructor: Deep copy\n";
    }
    Derived& operator=(const Derived& other) {
        if (this != &other) {
            delete data; 
            data = new int(*(other.data)); 
            std::cout << "Derived Assignment Operator: Deep copy\n";
        }
        return *this;
    }
    void display() const override {
        std::cout << "Derived class display function: Value = " << *data << "\n";
    }
    Derived operator+(const Derived& other) {
        std::cout << "Derived + operator overloaded\n";
        return Derived(*data + *(other.data));
    }
    ~Derived() {
        delete data;
        std::cout << "Derived Destructor: Freed memory\n";
    }
};
int main() {
    Derived obj1(10), obj2(20);
    Derived obj3 = obj1 + obj2; 
    obj3.display();
    Base* ptr = new Derived(50); 
    ptr->display(); 
    delete ptr; 
    return 0;
}

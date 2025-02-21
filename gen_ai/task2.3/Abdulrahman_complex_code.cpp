// i tried to make very complex code for chatGPT
// let's see my c++ skills!
// im thinking of
    //operator overloading
    //inheritance (overriding)
    //and of course pointers......

    //Code of complex_code.cpp:
    //By: Abdulrahman ALharbi 
    // i tried to make very complex code for chatGPT 
    // let's see my c++ skills! 
    // im thinking of 
        //operator overloading
        //inheritance (overriding)
        //and of course pointers......
#include <iostream>
#include <memory>
/*
Benefits of the Refactored Code
- Automatic Memory Management

Uses std::unique_ptr<int> to avoid manual new and delete.
- Eliminates Destructor

Since std::unique_ptr automatically frees memory, Derived no longer needs an explicit destructor.
- Maintains Deep Copy Logic

The copy constructor and assignment operator now rely on std::make_unique<int>() for deep copies.
- Improved Exception Safety

Avoids potential memory leaks by using smart pointers.
- More Readable and Maintainable

Cleaner, modern C++ approach.
*/
class Base {
public:
    virtual void display() const { 
        std::cout << "Base class display function\n"; 
    }
    virtual ~Base() { std::cout << "Base Destructor\n"; }
};

class Derived : public Base {
private:
    std::unique_ptr<int> data; 
public:
    Derived(int val) : data(std::make_unique<int>(val)) {
        std::cout << "Derived Constructor: Allocated memory\n";
    }
    Derived(const Derived& other) : data(std::make_unique<int>(*other.data)) {
        std::cout << "Derived Copy Constructor: Deep copy\n";
    }
    Derived& operator=(const Derived& other) {
        if (this != &other) {
            data = std::make_unique<int>(*other.data);
            std::cout << "Derived Assignment Operator: Deep copy\n";
        }
        return *this;
    }
    void display() const override {
        std::cout << "Derived class display function: Value = " << *data << "\n";
    }
    Derived operator+(const Derived& other) {
        std::cout << "Derived + operator overloaded\n";
        return Derived(*data + *other.data);
    }
};

int main() {
    Derived obj1(10), obj2(20);
    Derived obj3 = obj1 + obj2; 
    obj3.display();

    std::unique_ptr<Base> ptr = std::make_unique<Derived>(50);
    ptr->display(); 

    return 0;
}

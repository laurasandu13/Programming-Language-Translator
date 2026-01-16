class Person {
    private String name;
    private int age;
    
    Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    void greet() {
        System.out.println("Hello, I am " + this.name);
    }
    
    void haveBirthday() {
        this.age++;
        System.out.println(this.name + " is now " + this.age);
    }
    
    boolean isAdult() {
        if (this.age >= 18) {
            return true;
        } else {
            return false;
        }
    }
}

class Dog {
    private String name;
    private int age;
    
    Dog(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    void bark() {
        System.out.println(this.name + " says: Woof!");
    }
    
    int getDogYears() {
        int dogYears = this.age * 7;
        return dogYears;
    }
}

public class SimpleClassTest {
    public static void main(String[] args) {
        System.out.println("=== CLASS DEMO ===");
        
        Person alice = new Person("Alice", 25);
        alice.greet();
        alice.haveBirthday();
        
        boolean isAliceAdult = alice.isAdult();
        if (isAliceAdult) {
            System.out.println("Alice is an adult");
        }
        
        Dog buddy = new Dog("Buddy", 3);
        buddy.bark();
        int years = buddy.getDogYears();
        System.out.println("Dog years: " + years);
        
        System.out.println("=== DONE ===");
    }
}

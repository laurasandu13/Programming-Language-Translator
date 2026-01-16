import java.util.Scanner;

public class UserInputDemo {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("=== USER INPUT DEMONSTRATION ===");
        
        // String input using nextLine
        System.out.println("Enter your full name:");
        String fullName = scanner.nextLine();
        
        // Integer input
        System.out.println("Enter your age:");
        int age = scanner.nextInt();
        
        // Double input
        System.out.println("Enter your GPA (e.g., 3.75):");
        double gpa = scanner.nextDouble();
        
        // Float input
        System.out.println("Enter your height in meters (e.g., 1.75):");
        float height = scanner.nextFloat();
        
        // Single word string input
        System.out.println("Enter your favorite programming language:");
        String language = scanner.next();
        
        // Display all collected information
        System.out.println("\n=== YOUR INFORMATION ===");
        System.out.println("Name: " + fullName);
        System.out.println("Age: " + age);
        System.out.println("GPA: " + gpa);
        System.out.println("Height: " + height + " meters");
        System.out.println("Favorite Language: " + language);
        
        // Conditional logic based on user input
        System.out.println("\n=== ANALYSIS ===");
        
        if (age >= 18) {
            System.out.println("You are an adult.");
        } else {
            System.out.println("You are a minor.");
        }
        
        if (gpa >= 3.5) {
            System.out.println("Excellent GPA! You're on the Dean's List.");
        } else if (gpa >= 3.0) {
            System.out.println("Good GPA! Keep up the good work.");
        } else if (gpa >= 2.5) {
            System.out.println("Average GPA. Room for improvement.");
        } else {
            System.out.println("GPA needs attention.");
        }
        
        // Simple calculation with user input
        int yearsToGraduation = 22 - age;
        if (yearsToGraduation > 0) {
            System.out.println("Estimated years until typical graduation: " + yearsToGraduation);
        } else {
            System.out.println("You are past typical graduation age.");
        }
        
        scanner.close();
        System.out.println("\n=== DEMO COMPLETE ===");
    }
}

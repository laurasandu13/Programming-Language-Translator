public class Input {
    public static void main(String[] args) {
        // Variable declarations - all supported types
        int count = 0;
        int max = 10;
        String message = "Hello from Java";
        char initial = 'A';
        float price = 19.99f;
        double pi = 3.14159;
        boolean isActive = true;
        boolean isDone = false;
        
        // Print statements
        System.out.println("Starting translation test");
        System.out.println(message);
        System.out.println(count);
        
        // Simple if statement
        if (count < max) {
            System.out.println("Count is less than max");
        }
        
        // If-else statement
        if (isActive) {
            System.out.println("System is active");
        } else {
            System.out.println("System is inactive");
        }
        
        // If-else-if-else chain
        int score = 85;
        if (score >= 90) {
            System.out.println("Grade A");
        } else if (score >= 80) {
            System.out.println("Grade B");
        } else if (score >= 70) {
            System.out.println("Grade C");
        } else {
            System.out.println("Grade F");
        }
        
        // Logical operators - AND
        int age = 25;
        boolean hasLicense = true;
        if (age >= 18 && hasLicense) {
            System.out.println("Can drive");
        }
        
        // Logical operators - OR
        boolean isWeekend = false;
        boolean isHoliday = true;
        if (isWeekend || isHoliday) {
            System.out.println("Day off");
        }
        
        // Complex logical condition
        int temperature = 75;
        boolean isSunny = true;
        if ((temperature > 70 && temperature < 85) && isSunny) {
            System.out.println("Perfect weather");
        }
        
        // While loop - simple
        int i = 0;
        while (i < 5) {
            System.out.println(i);
            i++;
        }
        
        // While loop with complex condition
        int x = 0;
        int y = 10;
        while (x < 5 && y > 5) {
            x++;
            y--;
        }
        
        // For loop - counting up
        for (int j = 0; j < 5; j++) {
            System.out.println(j);
        }
        
        // For loop - counting down
        for (int k = 10; k > 0; k--) {
            System.out.println(k);
        }
        
        // For loop with <= operator
        for (int m = 1; m <= 5; m++) {
            System.out.println(m);
        }
        
        // For loop with different types
        for (int counter = 0; counter < 3; counter++) {
            System.out.println("Loop iteration");
        }
        
        // Nested if in for loop
        for (int n = 0; n < 10; n++) {
            if (n == 5) {
                System.out.println("Halfway");
            }
        }
        
        // Increment/decrement operators
        int value = 5;
        value++;
        System.out.println(value);
        value--;
        System.out.println(value);
        
        // Multiple conditions
        int num = 42;
        if (num > 0) {
            if (num < 100) {
                System.out.println("Number in range");
            }
        }
        
        // Boolean variable as condition
        boolean flag = true;
        if (flag) {
            System.out.println("Flag is true");
        }
        
        // Comparison operators
        int a = 10;
        int b = 20;
        if (a == b) {
            System.out.println("Equal");
        }
        if (a != b) {
            System.out.println("Not equal");
        }
        if (a < b) {
            System.out.println("Less than");
        }
        if (a > b) {
            System.out.println("Greater than");
        }
        if (a <= b) {
            System.out.println("Less or equal");
        }
        if (a >= b) {
            System.out.println("Greater or equal");
        }
        
        // Final test message
        System.out.println("Translation test complete");
    }
}

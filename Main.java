public class Main {
    public static void main(String[] args) {
        // Variable declarations - all types
        int count = 0;
        String message = "Hello";
        char letter = 'A';
        float price = 9.99f;
        double pi = 3.14;
        boolean isActive = true;
        
        // If-else-if chain
        int score = 85;
        if (score >= 90) {
            System.out.println("A");
        } else if (score >= 80) {
            System.out.println("B");
        } else if (score >= 70) {
            System.out.println("C");
        } else {
            System.out.println("F");
        }
        
        // While loop with increment
        int i = 0;
        while (i < 3) {
            System.out.println(i);
            i++;
        }
        
        // While loop with decrement
        int j = 5;
        while (j > 2) {
            System.out.println(j);
            j--;
        }
        
        // For loop with <
        for (i = 0; i < 4; i++) {
            System.out.println(i);
        }
        
        // For loop with <=
        for (i = 1; i <= 3; i++) {
            System.out.println(i);
        }
        
        // For loop with > (decrement)
        for (i = 5; i > 2; i--) {
            System.out.println(i);
        }
        
        // For loop with >= (decrement)
        for (i = 4; i >= 1; i--) {
            System.out.println(i);
        }
        
        // Nested loops with if
        int outer = 0;
        while (outer < 2) {
            int inner = 0;
            for (inner = 0; inner < 2; inner++) {
                if (outer == inner) {
                    System.out.println("Equal");
                } else {
                    System.out.println("Different");
                }
            }
            outer++;
        }
        
        // Complex condition with && and ||
        int x = 5;
        int y = 10;
        if (x < 10 && y > 5) {
            System.out.println("Both true");
        }
        
        if (x > 10 || y > 5) {
            System.out.println("At least one true");
        }
        
        // Nested if with while
        int num = 0;
        while (num < 5) {
            if (num < 2) {
                System.out.println("Small");
            } else {
                if (num == 3) {
                    System.out.println("Three");
                } else {
                    System.out.println("Other");
                }
            }
            num++;
        }
        
        // True/false literals
        boolean flag = false;
        if (flag) {
            System.out.println("True branch");
        } else {
            System.out.println("False branch");
        }
    }
}

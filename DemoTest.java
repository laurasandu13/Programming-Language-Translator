public static void main(String[] args) {
    System.out.println("=== JAVA-TO-PYTHON TRANSLATOR DEMO ===");
    
    System.out.println("\n=== SECTION 1: VARIABLES ===");
    int count = 10;
    double pi = 3.14159;
    float temperature = 98.6f;
    String message = "Hello World";
    char grade = 'A';
    boolean isActive = true;
    
    System.out.println("Integer: " + count);
    System.out.println("Double: " + pi);
    System.out.println("Float: " + temperature);
    System.out.println("String: " + message);
    System.out.println("Char: " + grade);
    System.out.println("Boolean: " + isActive);
    
    System.out.println("\n=== SECTION 2: IF-ELSE STATEMENTS ===");
    int age = 25;
    System.out.println("Age: " + age);
    
    if (age >= 18) {
        System.out.println("You are an adult");
    }
    
    if (age >= 21) {
        System.out.println("Can drink in US");
    } else {
        System.out.println("Cannot drink in US");
    }
    
    int score = 85;
    System.out.println("Score: " + score);
    if (score >= 90) {
        System.out.println("Grade: A");
    } else if (score >= 80) {
        System.out.println("Grade: B");
    } else if (score >= 70) {
        System.out.println("Grade: C");
    } else {
        System.out.println("Grade: F");
    }
    
    boolean hasLicense = true;
    if (age >= 16 && hasLicense) {
        System.out.println("Can drive!");
    }
    
    boolean isWeekend = true;
    boolean isHoliday = false;
    if (isWeekend || isHoliday) {
        System.out.println("Day off!");
    }
    
    int temp = 75;
    boolean isSunny = true;
    if (temp > 70 && temp < 85 && isSunny) {
        System.out.println("Perfect weather!");
    }
    
    System.out.println("\n=== SECTION 3: SWITCH STATEMENTS ===");
    int day = 3;
    System.out.println("Day number: " + day);
    switch(day) {
        case 1:
            System.out.println("Monday");
            break;
        case 2:
            System.out.println("Tuesday");
            break;
        case 3:
            System.out.println("Wednesday");
            break;
        case 4:
            System.out.println("Thursday");
            break;
        case 5:
            System.out.println("Friday");
            break;
        default:
            System.out.println("Weekend");
    }
    
    int month = 7;
    System.out.println("Month number: " + month);
    switch(month) {
        case 12:
        case 1:
        case 2:
            System.out.println("Winter");
            break;
        case 3:
        case 4:
        case 5:
            System.out.println("Spring");
            break;
        case 6:
        case 7:
        case 8:
            System.out.println("Summer");
            break;
        case 9:
        case 10:
        case 11:
            System.out.println("Fall");
            break;
    }
    
    char operation = '+';
    int num1 = 15;
    int num2 = 5;
    System.out.println("Calculator test:");
    switch(operation) {
        case '+':
            int addResult = num1 + num2;
            System.out.println("Addition result: " + addResult);
            break;
        case '-':
            int subResult = num1 - num2;
            System.out.println("Subtraction result: " + subResult);
            break;
        case '*':
            int mulResult = num1 * num2;
            System.out.println("Multiplication result: " + mulResult);
            break;
        case '/':
            int divResult = num1 / num2;
            System.out.println("Division result: " + divResult);
            break;
    }
    
    System.out.println("\n=== SECTION 4: WHILE LOOPS ===");
    int i = 1;
    while (i <= 5) {
        System.out.println("Count: " + i);
        i++;
    }
    
    int x = 0;
    int y = 10;
    while (x < 3 && y > 5) {
        System.out.println("x=" + x + " y=" + y);
        x++;
        y--;
    }
    
    System.out.println("\n=== SECTION 5: FOR LOOPS ===");
    for (int j = 0; j < 5; j++) {
        System.out.println("Iteration: " + j);
    }
    
    for (int k = 5; k > 0; k--) {
        System.out.println("Countdown: " + k);
    }
    
    for (int m = 1; m <= 3; m++) {
        System.out.println("Step " + m + " of 3");
    }
    
    for (int n = 0; n < 10; n++) {
        if (n == 5) {
            System.out.println("Halfway at " + n);
        }
    }
    
    System.out.println("\n=== SECTION 6: INCREMENT/DECREMENT ===");
    int value = 10;
    System.out.println("Initial: " + value);
    value++;
    System.out.println("After increment: " + value);
    value--;
    System.out.println("After decrement: " + value);
    
    System.out.println("\n=== SECTION 7: COMPARISON OPERATORS ===");
    int a = 10;
    int b = 20;
    System.out.println("a=" + a + " b=" + b);
    
    if (a == b) {
        System.out.println("a equals b");
    }
    if (a != b) {
        System.out.println("a not equal b");
    }
    if (a < b) {
        System.out.println("a less than b");
    }
    if (a <= b) {
        System.out.println("a less or equal b");
    }
    if (a > b) {
        System.out.println("a greater than b");
    }
    if (a >= b) {
        System.out.println("a greater or equal b");
    }
    
    System.out.println("\n=== DEMO COMPLETE ===");
}

public class HelloWorld {
    public static void main(String[] args) {
        // String name = "Jane";
        // System.out.println(name);

        // double d = 5.4;
        // System.out.println(d);

        // float f = 5.4f;
        // System.out.println(f);

        // char c = 'm';
        // System.out.println(c);

        int score = 85;
        boolean attended = true;
        int attempts = 3;

        if (score >= 90 && attended) {
            System.out.println("Grade: A+");
        } else if (score >= 80) {
            System.out.println("Grade: B");
        } else if (score >= 70 || attempts > 2) {
            System.out.println("Grade: C");
        } else if (score >= 60) {
            System.out.println("Grade: D");
        } else {
            System.out.println("Grade: F - Failed");
        }

    }
}
import java.util.Scanner;
import java.util.Stack;

/**
 * An implementation of a postfix calculator
 */
public class PostfixCalculator {
 
 /**
  * The implementation of a postfix calculator
  * @param args
  */
 public static void main(String[] args)
 {
  Scanner scan = new Scanner(System.in);
  Stack<Double> postfix = new Stack();
  String[] line = scan.nextLine().split(" ");
  for(int i = 0; i < line.length; i++)
  {
    if (line[i] == "+") {
      double j = postfix.pop();
      double j2 = postfix.pop();
      double sum = j + j2;
      postfix.push(sum);
    }
    else if (line[i] == "-") {
      double j = postfix.pop();
      double j2 = postfix.pop();
      double sub = j2 - j;
      postfix.push(sub);
    }
    else if (line[i] == "*") {
      double j = postfix.pop();
      double j2 = postfix.pop();
      double mult = j2 * j;
      postfix.push(mult);
    }
    else if (line[i] == "/") {
      double j = postfix.pop();
      double j2 = postfix.pop();
      double div = j2 / j;
      postfix.push(div);
    }
    else
      postfix.push(Double.parseDouble(line[i]));
    
  }
  
  System.out.println(postfix.pop());
 }
 
}

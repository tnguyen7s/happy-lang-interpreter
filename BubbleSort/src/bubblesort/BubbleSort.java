/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package bubblesort;

/**
 *
 * @author Tuyen
 */
import java.util.Scanner;
public class BubbleSort {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("How many number? ");
        int n =  scanner.nextInt();
        
        int[] array = new int[n];
        
        System.out.println("Enter "+ n + " numbers: ");
        for (int i=0; i<n; i++){
            array[i] = scanner.nextInt();
        }
        
        bubbleSort(array);
        
        System.out.println("Sorted: ");
        for (int i=0; i<n; i++){
            System.out.println(array[i]);
        }
    }
    
    public static void bubbleSort(int[] array){
       int tmp;
       boolean next = true;
        for (int i=0; i<array.length && next; i++){
            next=false;
            for (int j=0; j<array.length-1; j++){
               if (array[j]>array[j+1]){
                   next = true;
                   tmp = array[j];
                   array[j] = array[j+1];
                   array[j+1] = tmp;
               }             
           }
       }
    }
    
}

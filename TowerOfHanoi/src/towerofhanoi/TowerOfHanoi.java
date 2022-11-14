/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package towerofhanoi;

import java.util.Scanner;
import java.util.Stack;

/**
 *
 * @author Tuyen
 */
public class TowerOfHanoi {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("Enter number of disks: ");
        int n = scanner.nextInt();
        
        Stack<Integer> source = new Stack();
        Stack<Integer> aux = new Stack();
        Stack<Integer> target = new Stack();
        
        System.out.println("Disks in the source: ");
        for (int i=n; i>=1; i--){
            System.out.println(i);
            source.push(i);
        }
        
        move(n, source, target, aux);
        System.out.println("Disks in the target: ");
        for (int i=0; i<target.size(); i++){
            System.out.println(target.get(i));
        }
    }
    
    public static void move(int n, Stack<Integer> source, Stack<Integer> target, Stack<Integer> aux){
        if (n>0){
            move(n-1, source, aux, target);
        
            target.push(source.pop());
        
            move(n-1, aux, target, source);
        }

        
    }
    
}

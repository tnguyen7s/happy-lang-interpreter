/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package sudoku;

import java.util.HashSet;

/**
 *
 * @author Tuyen
 */
public class Sudoku {
    public static void main(String[] args) {
        int [][] grid= new int [9][9];
        int [] row1 = {1,0,2,0,0,0,0,0,0};
        int [] row2 = {0,0,0,0,0,0,0,0,0};
        int [] row3 = {2,0,3,0,0,0,0,0,0};
        int [] row4 = {3,0,0,4,0,0,0,0,0};
        int [] row5 = {0,0,0,0,0,0,0,0,0};
        int [] row6 = {0,0,0,7,0,0,0,0,0};
        int [] row7 = {0,0,0,0,0,0,0,0,0};
        int [] row8 = {0,0,0,0,0,0,0,0,0};
        int [] row9 = {0,0,0,0,0,0,0,0,0};


        grid[0] = row1;
        grid[1] = row2;
        grid[2] = row3;
        grid[3] = row4;
        grid[4] = row5;
        grid[5] = row6;
        grid[6] = row7;
        grid[7] = row8;
        grid[8] = row9;
        
        System.out.println(sudoku(0, 0, grid));
        
        for (int r=0; r<9; r++){
            for (int c=0; c<9; c++){
                System.out.print(grid[r][c]+" ");
            }
            System.out.println();
        }
    }
    
    public static boolean sudoku(int row, int col, int[][] grid){
        // when done
        if (row==9){
            return valid(8, 8, grid);
        }
                
        // pick a choice
        int nextRow = row;
        int nextCol = col;
        
        // for the case that the grid has values in it
        if (grid[row][col]!=0){
            if (col<8){
                nextRow = row;
                nextCol = col+1;
            }
            else{
                nextRow = row+1;
                nextCol = 0;
            }
            
            if (sudoku(nextRow, nextCol, grid)){
                return true;
            }
            else
            {
                return false;
            }
        }
        
        for (int val=1; val<=9; val++){
            grid[row][col] = val;
            
            // validate the choice, if not qualified, select the next choice
            if (!valid(row, col, grid)){
                continue;
            }
            
            // otherwise, if the choice is good, next spot
            if (col<8){
                nextRow = row;
                nextCol = col+1;
            }
            else{
                nextRow = row+1;
                nextCol = 0;
            }
            
            if (sudoku(nextRow, nextCol, grid)){
                return true;
            }

        }
        
        grid[row][col]=0;
        return false;
    }
    
    public static boolean valid(int row, int col, int[][] grid){
        // check the row
        HashSet<Integer> set = new HashSet<>();
        int val;
        for (int i=0; i<=col; i++){
            val = grid[row][i];
            if (set.contains(val)){
                return false;
            }
            
            set.add(val);
        }
        
        // check column
        set.clear();
        for (int j=0; j<=row; j++){
            val = grid[j][col];
            
            if (set.contains(val)){
                return false;
            }
            
            set.add(val);
        }
        
        // check grid
        // 0 1 2 3 4 5 6 7 8 
        // 1
        set.clear();
        int fromRow = (row/3)*3;
        int toRow = (row/3)*3+row%3;
        int fromCol = (col/3)*3;
        int toCol = (col/3)*3+col%3;
        
        for (int r=fromRow; r<=toRow; r++){
           for (int c=fromCol; c<=toCol; c++){
               val = grid[r][c];
               
               if (set.contains(val)){
                   return false;
               }
               
               set.add(val);
           }
        }
        
        return true;
    }
    
}

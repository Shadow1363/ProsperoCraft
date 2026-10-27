/* SPDX-License-Identifier: MIT
 * ProsperoCraft controller keyboard layout shared by SDL input and WSI overlay. */
#ifndef PROSPERO_KEYBOARD_LAYOUT_H
#define PROSPERO_KEYBOARD_LAYOUT_H
static inline char prospero_keyboard_character(int selected,int lower,int symbols)
{
 static const char normal[]="1234567890""qwertyuiop""asdfghjkl;""zxcvbnm,.-"" :/_@+!?()";
 static const char special[]="1234567890""!@#$%^&*()""[]{}<>\\|~=""`$%&*+\"',."" :/_@+!?()";
 if(selected<0||selected>=50)return 0;
 char c=(symbols?special:normal)[selected];if(!lower&&c>='a'&&c<='z')c-=32;return c;
}
static inline int prospero_keyboard_move(int selected,int direction)
{
 if(selected<0||selected>55)selected=10;
 int row=selected<50?selected/10:5,col=selected<50?selected%10:selected-50,columns=row==5?6:10;
 if(direction==-1)col=(col+columns-1)%columns;
 else if(direction==1)col=(col+1)%columns;
 else if(direction==-10){if(row==5){row=4;col=col*10/6;}else if(row>0)row--;}
 else if(direction==10){if(row==4){row=5;col=col*6/10;}else if(row<4)row++;}
 return row==5?50+col:row*10+col;
}
#endif

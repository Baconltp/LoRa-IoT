 
 f r o m   p y b   i m p o r t   P i n  
 p _ i n   =   P i n ( ' X 1 2 ' , P i n . I N , P i n . P U L L _ U P )  
  
 a d c   =   p y b . A D C ( P i n ( ' X 1 1 ' ) )  
 a d c   =   p y b . A D C ( p y b . P i n . b o a r d . X 1 1 )  
  
 d e f   g e t R a i n A o ( ) :  
         r e t u r n   a d c . r e a d ( )  
  
 d e f   g e t R a i n D O ( ) :  
         r e t u r n   p _ i n . v a l u e 
#include<Wire.h>
#include <S11059.h>

S11059 colorSensor;
int r,g,b,a,R,G,B,out;
int a0=5;
int a1=4;
float arr[4];

void setup(){
  Wire.begin();
  Serial.begin(115200);
  Wire.beginTransmission(0x2A);
  Wire.write(0x0);
  Wire.write(0x89);
  Wire.endTransmission();
  Wire.beginTransmission(0x2A);
  Wire.write(0x0);
  Wire.write(0x09);
  Wire.endTransmission();
}
void loop(){
  int data = Serial.read();
  if (data == 'a'){
    READ();
  }
}
void READ(){
  colorread();
  arr[0]=r;
  arr[1]=g;
  arr[2]=b;
  arr[3]=a;
  Serial.write(colored(arr));
}
void colorread(){
  int h,l;
  Wire.beginTransmission(0x2A);
  Wire.write(0x03);
  Wire.endTransmission();
  Wire.requestFrom(0x2A,8);
  if(Wire.available()){
    h = Wire.read();
    l = Wire.read();
    r = h << 8|l;
    
    h = Wire.read();
    l = Wire.read();
    g = h << 8|l;
    
    h = Wire.read();
    l = Wire.read();
    b = h << 8|l;
    
    h = Wire.read();
    l = Wire.read();
    a = h << 8|l;
   
  }
  Wire.endTransmission();
}
int colored(float *arr){
  float color[6][3] = {{6.23875, 4.9325, 4.2125},
                       {3.47375, 12.06875, 5.5},
                       {9.88875, 4.69125, 2.87},
                       {2.88375, 6.4825, 8.395},
                       {5.41875, 11.66875, 4.09},
                       {4.67, 8.27, 7.03}};
  float R = arr[0]/arr[3];
  float G = arr[1]/arr[3];
  float B = arr[2]/arr[3];
  /*Serial.print(R);
  Serial.println("");
  Serial.print(G);
  Serial.println("");
  Serial.print(B);
  Serial.println("");*/
  float temp = 10000; 
  int result = -1;
  float r, g, b, ave, work;
  for (int i=0;i<6;i++){
    r = R / color[i][0];
    g = G / color[i][1];
    b = B / color[i][2];
    ave = (r + g + b) / 3;
    work = (r-ave)*(r-ave) + (g-ave)*(g-ave) + (b-ave)*(b-ave);
    if (work < temp){
      temp = work;
      result = i;
    }
  }
  return result;
}
int ChgI2CMultiplexer(unsigned char adrs,unsigned char ch)
{
     unsigned char c ;
     int  ans ;

     Wire.beginTransmission(adrs) ;     // 通信の開始
     c = ch & 0x07 ;                    // チャネル(bit0-2)を取り出す
     c = c | 0x08 ;                     // enableビットを設定する
     Wire.write(c) ;                    // Control register の送信
     ans = Wire.endTransmission() ;     // データの送信と通信の終了
     
     
     return ans ;
}

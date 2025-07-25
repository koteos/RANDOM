// Puertos
const int botonSumaPin = 12;    //boton que sumara 5 al ciclo de trabajo
const int botonSuma2Pin = 10;   
const int ledPin = 5;    
const int AD = 2;
const int AT = 3;//Puerto con salida PWM

// Variables
int botonSumaValue;           //Variable para el boton de suma
int botonRestaValue;          //Variable para el boton de resta
int botonSuma2Value;  
int cicloTrabajo;   
int Rele1 =0;
int Rele2=0;  

//inicialización
void setup(){
  Serial.begin (9600);
  pinMode(ledPin, OUTPUT);
  pinMode(botonSumaPin, INPUT);
  pinMode(botonSuma2Pin, INPUT);
  pinMode(AD,OUTPUT);
  pinMode(AT,OUTPUT);
}

void loop (){
  
  botonSumaValue= digitalRead(botonSumaPin);
  botonSuma2Value= digitalRead(botonSuma2Pin);
  botonRestaValue= !(botonSumaValue | botonSuma2Value); 
  
  Serial.println(botonRestaValue, DEC);
  
 

  if (botonSumaValue == HIGH and botonSuma2Value == LOW  && cicloTrabajo <=250){
    cicloTrabajo +=5;
    digitalWrite(AD,HIGH);
  }
  if (botonSumaValue == LOW and botonSuma2Value == HIGH  && cicloTrabajo <=250){
    cicloTrabajo +=5;
    digitalWrite(AT,HIGH); 
  }
  if (botonRestaValue == HIGH && cicloTrabajo >=5){
    cicloTrabajo -=5;
  }
  if(cicloTrabajo<=5){
    digitalWrite(AD,LOW);
    digitalWrite(AT,LOW);
  }
  analogWrite(ledPin, cicloTrabajo);
  delay(50);
  
}

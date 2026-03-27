/*
* PROYECTO: Sistema de Gravedad Cero - Control de Polipasto
 * VERSIÓN: 1.0 Protección contra Desconexión de Sensor con Filtro digital
 * FECHA: 09 - Enero - 2026
 * AUTOR: Omar López Cruz
 * COMPAÑIA: KOTEMAH
 */

#include "HX711.h"

// =============================================================================
// 1. CONFIGURACIÓN DE PINES
// =============================================================================
#define PIN_RELE_BAJADA 2    // Salida Relevador 1
#define PIN_RELE_SUBIDA 3    // Salida Relevador 2
#define HX711_DT        4    // Bus de Datos Sensor
#define HX711_SCK       5    // Reloj Sensor
#define PIN_SALIDA_PWM  A0   // Salida Control Velocidad (0-3.3V/5V)

// =============================================================================
// 2. PARAMETROS DE CALIBRACIÓN Y CARGA
// =============================================================================
// Ajustar este valor con peso conocido para calibrar la báscula
#define FACTOR_CALIBRACION  48621.0 

#define CARGA_NOMINAL       20.0    // Peso objetivo del sistema (Kg)
#define UMBRAL_HISTERESIS   1.0     // Zona muerta de activación (+/- Kg)
#define LIMITE_ERROR_SENSOR -0.20   // Umbral de seguridad para desconexión

// =============================================================================
// 3. AJUSTE DE RESPUESTA (MOTOR Y FILTRO)
// =============================================================================
const int PASO_RAMPA = 30;     // Velocidad de reacción del PWM 
#define FACTOR_FILTRO  0.6     // Suavizado de señal (0.1 = Lento, 1.0 = Directo)
#define TIMEOUT_SEGURIDAD 150  // Tiempo máximo sin señal (ms)

// --- Variables del Sistema ---
HX711 balanza;
float masaReferencia = CARGA_NOMINAL;
float pesoFiltrado = 0;
int valorDAC = 0;
unsigned long tiempoUltimaLectura = 0;

void setup() {
  // Inicialización de Puertos
  pinMode(PIN_SALIDA_PWM, OUTPUT);
  pinMode(PIN_RELE_BAJADA, OUTPUT);
  pinMode(PIN_RELE_SUBIDA, OUTPUT);
  
  digitalWrite(PIN_RELE_BAJADA, LOW);
  digitalWrite(PIN_RELE_SUBIDA, LOW);
  analogWriteResolution(8); 
  analogWrite(PIN_SALIDA_PWM, 0);

  Serial.begin(115200);

  // Inicialización Sensor
  balanza.begin(HX711_DT, HX711_SCK);  
  balanza.set_scale(FACTOR_CALIBRACION); 

  // Tara Inicial al arranque
  if (balanza.wait_ready_timeout(1000)) {
    masaReferencia = balanza.get_units(10);
    pesoFiltrado = masaReferencia; // Precarga del filtro
    Serial.println("Sistema en Linea.");
  } else {
    masaReferencia = CARGA_NOMINAL;
    pesoFiltrado = CARGA_NOMINAL;
  }
  
  tiempoUltimaLectura = millis();
}

void loop() {
  // Lectura Non-Blocking
  if (balanza.is_ready()) {
    tiempoUltimaLectura = millis();
    
    // Adquisición y Filtrado EMA
    float lecturaRaw = balanza.get_units(1);
    pesoFiltrado = (lecturaRaw * FACTOR_FILTRO) + (pesoFiltrado * (1.0 - FACTOR_FILTRO));

    // --- LÓGICA DE CONTROL ---

    // 1. Error de Sensor (Seguridad)
    if (lecturaRaw < LIMITE_ERROR_SENSOR) {
       gestionFrenado();
    }
    
    // 2. Asistencia en BAJADA
    else if (pesoFiltrado > masaReferencia + UMBRAL_HISTERESIS) {
      digitalWrite(PIN_RELE_BAJADA, HIGH);
      digitalWrite(PIN_RELE_SUBIDA, LOW);
      
      if (valorDAC < 255) {
        valorDAC += PASO_RAMPA;
        if (valorDAC > 255) valorDAC = 255;
        analogWrite(PIN_SALIDA_PWM, valorDAC);
      }
    }
    
    // 3. Asistencia en SUBIDA
    else if (pesoFiltrado < masaReferencia - UMBRAL_HISTERESIS) {
      digitalWrite(PIN_RELE_BAJADA, LOW);
      digitalWrite(PIN_RELE_SUBIDA, HIGH);
      
      if (valorDAC < 255) {
        valorDAC += PASO_RAMPA;
        if (valorDAC > 255) valorDAC = 255;
        analogWrite(PIN_SALIDA_PWM, valorDAC);
      }
    }
    
    // 4. Zona de Equilibrio
    else {
      gestionFrenado();
    }
  }

  // Parada de emergencia por fallo de comunicación
  if (millis() - tiempoUltimaLectura > TIMEOUT_SEGURIDAD) {
    valorDAC = 0;
    analogWrite(PIN_SALIDA_PWM, 0);
    digitalWrite(PIN_RELE_BAJADA, LOW);
    digitalWrite(PIN_RELE_SUBIDA, LOW);
  }
}

// Rutina de desaceleración y corte
void gestionFrenado() {
  if (valorDAC > 0) {
    valorDAC -= PASO_RAMPA;
    if (valorDAC < 0) valorDAC = 0;
    analogWrite(PIN_SALIDA_PWM, valorDAC);
  }
  
  // Apagar relés solo cuando la potencia sea cero
  if (valorDAC == 0){
    digitalWrite(PIN_RELE_BAJADA, LOW);
    digitalWrite(PIN_RELE_SUBIDA, LOW);
  }
}
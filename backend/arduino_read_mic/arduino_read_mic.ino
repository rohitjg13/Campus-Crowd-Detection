void setup() {
    Serial.begin(115200);
}

void loop() {
    unsigned int sample1 = analogRead(A0);
//    unsigned int sample2 = analogRead(A1);
//    unsigned int sample3 = analogRead(A2);

    
    Serial.write(lowByte(sample1));
    Serial.write(highByte(sample1));

    delayMicroseconds(10);  // ~8kHz sample rate (1 sec / 8000 samples)
}
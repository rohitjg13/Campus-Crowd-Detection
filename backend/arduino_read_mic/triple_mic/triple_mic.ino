void setup() {
  Serial.begin(115200);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
}

int activeMic = 1; // Default to first microphone

void loop() {
  // Check if there's data available from Raspberry Pi
  if (Serial.available() > 0) {
    int command = Serial.read();
    // Update active microphone based on command
    if (command >= '1' && command <= '3') {
      activeMic = command - '0'; // Convert char to int
    }
  }
  
  // Read from the active microphone
  unsigned int sample;
  if (activeMic == 1) {
    sample = analogRead(A0);
  } else if (activeMic == 2) {
    sample = analogRead(A1);
  } else if (activeMic == 3) {
    sample = analogRead(A2);
  }
  
  // Send the sample data
  Serial.write(lowByte(sample));
  Serial.write(highByte(sample));
  delayMicroseconds(10); // ~8kHz sample rate
}
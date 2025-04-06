#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  Serial.begin(115200);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);

  // Initialize OLED display
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    // OLED not found
    while (true);
  }
display.clearDisplay();
display.setTextSize(2);
display.setTextColor(SSD1306_WHITE);

// Line 1
String line1 = "Campus";
int16_t x1 = (SCREEN_WIDTH - (line1.length() * 12)) / 2;
display.setCursor(x1, 0);
display.println(line1);

// Line 2
String line2 = "Crowd";
int16_t x2 = (SCREEN_WIDTH - (line2.length() * 12)) / 2;
display.setCursor(x2, 20);
display.println(line2);

// Line 3
String line3 = "Detection";
int16_t x3 = (SCREEN_WIDTH - (line3.length() * 12)) / 2;
display.setCursor(x3, 40);
display.println(line3);

display.display();
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
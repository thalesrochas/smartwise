void setup() {
    Serial.begin(9600);
    for (int i = 13; i > 7; i--) {
        pinMode(i, OUTPUT);
        digitalWrite(i, LOW);
    }
}

void loop() {
    unsigned int pin;
    unsigned int state;
    
    while (!Serial.available()) {}
    while (Serial.available()) {
        if (Serial.available()) {
            state = Serial.read();
        }
    }

    while (!Serial.available()) {}
    while (Serial.available()) {
        if (Serial.available()) {
            pin = int(Serial.read());
        }
    }

    pin += 7;

    if (state == 'H') {
        digitalWrite(pin, HIGH);
    }
    if (state == 'L') {
        digitalWrite(pin, LOW);
    }
}
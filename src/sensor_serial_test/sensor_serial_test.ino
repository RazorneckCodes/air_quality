
void setup() {
  Serial.begin(9600);
  Serial.println("Ready");
}

void loop() {
  while(Serial.available()){
    Serial.write(0x86);
    char c = Serial.read();
    
    if(c > 0){
      Serial.println(c);

    }
  }
  delay(2000);

}

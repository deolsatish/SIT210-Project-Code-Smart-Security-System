// This #include statement was automatically added by the Particle IDE.
#include <MQTT.h>

void callback(char* topic, byte* payload, unsigned int length);
MQTT client("test.mosquitto.org", 1883, callback);
int intruder_boolean=0;
int led1 = D7;

// recieve message
void callback(char* topic, byte* payload, unsigned int length) {
    char p[length + 1];
    memcpy(p, payload, length);
    p[length] = NULL;

    if (!strcmp(p, "Intruder"))
    {
        Particle.publish("INTRUDERALERT","INTRUDER",PRIVATE);
        digitalWrite(led1, HIGH);
        delay(1000);
        digitalWrite(led1, LOW);
    }
        
    else if (!strcmp(p, "No_Intruder"))
    {
        Particle.publish("INTRUDERALERT","NO_INTRUDER",PRIVATE);
        digitalWrite(led1, HIGH);
        delay(1000);
        digitalWrite(led1, LOW);
    }
        
    else
    {
        Particle.publish("INTRUDERALERT","INTRUDER",PRIVATE);
        digitalWrite(led1, HIGH);
        delay(1000);
        digitalWrite(led1, LOW);
    }
        
}

void setup() {
    client.connect("ParticleArgon");
    client.subscribe("argonconnect");
    pinMode(D7,OUTPUT);

}

void loop() {
    
    client.loop();

}

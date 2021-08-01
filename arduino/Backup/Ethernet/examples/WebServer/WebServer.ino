#include <SD.h>
#include <SPI.h>
#include <Ethernet.h>

byte mac[] = {0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0x00};
byte ip[] = {192, 168, 0, 12};

EthernetServer server(80);

File LOG;

int pos = 0;
char c;


void setup() 
{
  Serial.begin(9600);

  Ethernet.begin(mac, ip);
  
  server.begin();
  
  Serial.print("IP address ");
  for (int x = 0; x < 3; x ++)
  {
    Serial.print(ip[x]);
    Serial.print(".");
  }
  Serial.println(ip[3]);
  

  while (!SD.begin(4)) 
  {
    Serial.println("initialization failed!");
    Serial.println("Insérez une carte");
    delay(2000);
  }
  Serial.println("initialization done.");
}


void loop() 
{
  EthernetClient client = server.available();
  if (client) 
  {
    Serial.println("new client");
  
    boolean currentLineIsBlank = true;
    while (client.connected()) 
    {
      if (client.available()) 
      {
        char c = client.read();
        // Serial.write(c);
        if (c == '\n' && currentLineIsBlank) 
        {
          
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: text/html");
          client.println("Connection: close");  // the connection will be closed after completion of the response
          client.println();
          client.println("<!DOCTYPE HTML>");
          client.println("<html>");
          client.println("<title>Liste des tags lus</title>");
          client.println("<h1>Liste des tags lus</h1></br>");
          
          if (SD.exists("RFID_LOG.csv"))
          {
            LOG = SD.open("RFID_LOG.csv", FILE_READ);
            if (LOG)
            {
              Serial.println("Fichier : ");
              pos = 0;
              while (!LOG.available())
              {
                LOG.seek(pos);
                c = LOG.read();
                Serial.print(c);
                pos ++;
              }
            }
            LOG.close();
          }
          else
          {
            client.println("Carte SD absente");
          }
   
          client.println("</html>");
          break;
        }
        if (c == '\n') 
        {
          currentLineIsBlank = true;
        } else if (c != '\r') 
        {
          currentLineIsBlank = false;
        }
      }
    }
    delay(1);
    client.stop();
    Serial.println("client disconnected");
    Ethernet.maintain();
  }
}


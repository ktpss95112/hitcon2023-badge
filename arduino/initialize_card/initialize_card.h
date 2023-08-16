#include <ESP8266WiFi.h>
#include <LiquidCrystal_I2C.h>
#include "master_config.h"


const size_t LCD_LINE_LENGTH = 16;
LiquidCrystal_I2C lcd(0x27, LCD_LINE_LENGTH, 2);
const int ERR_SLEEP = 2000;
const int NORMAL_SLEEP = 1000;
const int SHORT_SLEEP = 500;


void __strncpy_without_trailing_0(char *dest, const char *src, size_t n) {
    for (int i = 0; src[i] != '\0' && i < n; ++i) {
        dest[i] = src[i];
    }
}


void lcd_print(const char *str, int sleep) {
    Serial.println(str);  // for debugging

    static char cache[2][LCD_LINE_LENGTH + 1] = {0};

    size_t len = strnlen(str, 2 * LCD_LINE_LENGTH);
    if (len <= LCD_LINE_LENGTH) {
        if (strncmp(cache[0], str, LCD_LINE_LENGTH) != 0) {
            lcd.clear();
            lcd.setCursor(0, 0);
            lcd.print(str);
            strncpy(cache[0], str, LCD_LINE_LENGTH);
        }
    } else {
        char str2[LCD_LINE_LENGTH + 1] = {0};
        memset(str2, ' ', LCD_LINE_LENGTH);
        __strncpy_without_trailing_0(str2, str, LCD_LINE_LENGTH);
        if (strncmp(cache[0], str2, LCD_LINE_LENGTH) != 0) {
            lcd.setCursor(0, 0);
            lcd.print(str2);
            strncpy(cache[0], str2, LCD_LINE_LENGTH);
        }
        memset(str2, ' ', LCD_LINE_LENGTH);
        __strncpy_without_trailing_0(str2, str + LCD_LINE_LENGTH, LCD_LINE_LENGTH);
        if (strncmp(cache[1], str2, LCD_LINE_LENGTH) != 0) {
            lcd.setCursor(0, 1);
            lcd.print(str2);
            strncpy(cache[1], str2, LCD_LINE_LENGTH);
        }
    }

    delay(sleep);  // rate limit
}


WiFiClient tcp_client;
const char *server_for_uid_upload = "192.168.1.62";  // TODO: CHANGE ME
int port_for_uid_upload = 9999;  // TODO: CHANGE ME


void init_network() {
    int count = 0;
    char progress[] = {'|', '-'};
    size_t progress_len = sizeof(progress) / sizeof(char);
    char buf[LCD_LINE_LENGTH * 2 + 1] = {0};

    WiFi.begin(WIFI_SSID, WIFI_PASSWD);
    snprintf(buf, LCD_LINE_LENGTH * 2, "Connecting to WiFi (%c)", progress[count++ % progress_len]);
    lcd_print(buf, SHORT_SLEEP);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        snprintf(buf, LCD_LINE_LENGTH * 2, "Connecting to WiFi (%c)", progress[count++ % progress_len]);
        lcd_print(buf, 0);
    }
    lcd_print("", 0);

    while (!tcp_client.connect(server_for_uid_upload, port_for_uid_upload)) {
        delay(500);
        snprintf(buf, LCD_LINE_LENGTH * 2, "Error connect tcp, retry ... (%c)", progress[count++ % progress_len]);
        lcd_print(buf, 0);
    }
    lcd_print("", 0);
}

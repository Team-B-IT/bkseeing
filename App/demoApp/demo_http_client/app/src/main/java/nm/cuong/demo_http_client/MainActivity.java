package nm.cuong.demo_http_client;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.net.URLEncoder;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        this.connect();
    }

    public void connect() {
        URL url = null;
        HttpURLConnection conn = null;
        try {
            url = new URL("http", "192.168.69.8", 80, "");
        } catch (MalformedURLException e) {
            Toast.makeText(MainActivity.this, "MalformedURLException: " + e, Toast.LENGTH_LONG).show();
        }
        if (url != null) {
            try {
                conn = (HttpURLConnection) (url.openConnection());
            } catch (IOException e) {
                Toast.makeText(MainActivity.this, "IOException: " + e, Toast.LENGTH_LONG).show();
            }
        }
        if (conn != null) {
            try {
                conn.setRequestMethod("GET");
            } catch (ProtocolException e) {
                Toast.makeText(MainActivity.this, "IOException: " + e, Toast.LENGTH_LONG).show();
            }

            try {
                conn.setDoOutput(true);
                conn.setRequestProperty("Content-Type", "MIME");
                conn.setRequestProperty("charset", "utf-8");
//                conn.setRequestProperty("Content-Length", "10");
                OutputStreamWriter out = new OutputStreamWriter((OutputStream) conn.getOutputStream());
                out.write("Đặng Xuân Vương");
                out.close();
            } catch (IOException e) {
                Toast.makeText(MainActivity.this, "IOException: " + e, Toast.LENGTH_LONG).show();
            }

            try {
                int rescode = conn.getResponseCode();
//                Toast.makeText(MainActivity.this, "Request Code: " + Integer.toString(rescode) + " " + conn.getResponseMessage(), Toast.LENGTH_LONG).show();
                InputStreamReader in = new InputStreamReader((InputStream) conn.getContent());
                BufferedReader buff = new BufferedReader(in);
                String line, text = "";
                do {
                    line = buff.readLine();
                    if (line == null) {
                        break;
                    }
                    text = text + "\n" + line;
                } while (true);
                Toast.makeText(MainActivity.this, "Response Content: " + text, Toast.LENGTH_LONG).show();
            } catch (IOException e) {
                Toast.makeText(MainActivity.this, "IOException: " + e, Toast.LENGTH_LONG).show();
            }
            conn.disconnect();
            //Toast.makeText(MainActivity.this, "You are here!", Toast.LENGTH_LONG).show();
        }
    }
}

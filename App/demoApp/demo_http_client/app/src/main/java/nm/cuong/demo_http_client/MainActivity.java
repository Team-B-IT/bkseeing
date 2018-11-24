package nm.cuong.demo_http_client;

import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
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
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        String img_link = "/storage/emulated/0/vuong/1.png";
        this.connect(img_link);
    }

    public void readImgBuff(String img_link, HttpURLConnection conn) {
        try {
            DataOutputStream out = new DataOutputStream(conn.getOutputStream());
            File file = new File(img_link);
            FileInputStream fis = new FileInputStream(file);
            byte buff[] = new byte[(int)file.length()];
            fis.read(buff);
            out.write(buff);
            out.close();
        } catch (IOException e) {
            Toast.makeText(MainActivity.this, "IOException: " + e + e, Toast.LENGTH_LONG).show();
        }
    }

    public void connect(String img_link) {
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

            conn.setDoOutput(true);
            conn.setRequestProperty("Content-Type", "MIME");
            conn.setRequestProperty("charset", "utf-8");
            readImgBuff(img_link, conn);

            try {
                int rescode = conn.getResponseCode();
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
//                Toast.makeText(MainActivity.this, "Response Content: " + text, Toast.LENGTH_LONG).show();
            } catch (IOException e) {
                Toast.makeText(MainActivity.this, "IOException: " + e, Toast.LENGTH_LONG).show();
            }
            conn.disconnect();
        }
    }
}

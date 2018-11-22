package nm.cuong.demo_http_client;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Toast;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
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
        URL url;
        try {
            url = new URL("http", "192.168.69.17", 80, "");
            Toast.makeText(MainActivity.this, "4kjkj, d0^` ng0^'k", Toast.LENGTH_LONG).show();
            try {
                HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                urlConnection.setRequestMethod("POST");
//                urlConnection.setDoOutput(true);
//                urlConnection.setInstanceFollowRedirects(false);
               String query = URLEncoder.encode("Hello!", "utf-8");
//               InputStream response = urlConnection.getInputStream();
//                urlConnection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
//                urlConnection.setRequestProperty("charset", "utf-8");
//                urlConnection.setRequestProperty("Content-Length", Integer.toString(requestdata.length()));
//                urlConnection.setUseCaches(false);
//                try (DataOutputStream w = new DataOutputStream(urlConnection.getOutputStream())) {
//                    w.write(requestdata.getBytes());
//                }
                int code = urlConnection.getResponseCode();
                Toast.makeText(MainActivity.this, "Anh Vuong dep trai", Toast.LENGTH_LONG).show();
//                try {
//                    String tmp = urlConnection.getRequestMethod();
//                    Toast.makeText(MainActivity.this, tmp, Toast.LENGTH_LONG).show();
//                } finally {
//                    Toast.makeText(MainActivity.this, "ph: ", Toast.LENGTH_LONG).show();
//                    urlConnection.disconnect();
//                }
            } catch(IOException e) {
                Toast.makeText(MainActivity.this, "xxx: " + e, Toast.LENGTH_LONG).show();
            }
        } catch(MalformedURLException e) {
            Toast.makeText(MainActivity.this, "jav: " + e, Toast.LENGTH_LONG).show();
        }
    }

}

package nm.cuong.cameraexample;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.hardware.Camera;
import android.hardware.Camera.PictureCallback;
import android.os.Bundle;
import android.os.Environment;
import android.speech.tts.TextToSpeech;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.RadioGroup;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class MainActivity extends Activity{
    private Camera mCamera;
    private CameraPreview mPreview;
    private PictureCallback mPicture;
    private Button capture, start;
    private TextView tvReport;
    public Context myContext;
    private LinearLayout cameraPreview;
    public Bitmap bitmap_x418, bitmap_418y;
    //TTS object
    private TextToSpeech myTTS;
    public String string_report = "Xin chào"; //Thong bao cho nguoi dung
    public int MY_PARAMETER_CONTROL = 0;// tham so dieu khien viec khoi dong chi duoc 1 lan( nut khoi dong)
    public int CHECK_CAMERA_TYPE = 0; // Mac dinh dung CAM cua dien thoai di dong
    public int CHECK_TEST_CAMERA_INTERNAL = 1;


//=============================================================================//ham onCreate


    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        myContext = this;
        initialize();


    }


//=============================================================================//menu

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.menu, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if (item.getItemId() == R.id.itemChoseProCam)
            if (item.isChecked()){
                if (hasCamera(myContext)) {
                    // huy ket noi camera chuyen dung
                    // ket noi lai voi camera dien thoai
                    item.setChecked(false);
                    Toast.makeText(myContext, "Chuyển đổi về CAMERA điện thoại thành công", Toast.LENGTH_LONG).show();
                    CHECK_CAMERA_TYPE = 0;
                }
                else {
                    Toast.makeText(myContext, "CAMERA điện thoại không khả dụng", Toast.LENGTH_LONG).show();
                }
            }
            else {
                item.setChecked(true);
//                if (hasProCamera()){
                // huy ket noi camera dien thoai
                // ket noi voi camera chuyen dung
//                    item.setChecked(true);
//                    Toast.makeText(myContext, "Chuyển đổi về CAMERA chuyên dụng", Toast.LENGTH_LONG).show();
//                    CHECK_CAMERA_TYPE = 1;
//                }
//                else {
//                    Toast.makeText(myContext, "CAMERA chuyên dụng không được tìm thấy", Toast.LENGTH_LONG).show();
//                }

            }
        else if (item.getItemId() == R.id.itemFinish){
            onDestroy();
            finish();
        }
        return (super.onOptionsItemSelected(item));
    }

//=============================================================================//ham he thong


    public void onResume() {
        super.onResume();
        if (CHECK_CAMERA_TYPE == 0){
            if (!hasCamera(myContext)) {
                Toast toast = Toast.makeText(myContext, "Sorry, your phone does not have a camera!", Toast.LENGTH_LONG);
                toast.show();
                finish();
            }
            if (mCamera == null) {
                mCamera = Camera.open(0);
                mPicture = getPictureCallback();
                mPreview.refreshCamera(mCamera);
            }
        }
        else {

        }

    }
    @Override
    protected void onPause() {
        super.onPause();
        //when on Pause, release camera in order to be used from other applications
        releaseCamera();
    }
    @Override
    protected void onDestroy() {
        super.onDestroy();
        releaseCamera();
    }

    @Override
    protected void onRestart() {
        super.onRestart();
        releaseCamera();
    }

//=============================================================================//ham khoi tao ban dau


    public void initialize() {
        myTTS = new TextToSpeech (MainActivity.this, new TextToSpeech.OnInitListener(){
            @Override
            public void onInit(int status) {
                if (status != TextToSpeech.ERROR){
                    myTTS.setLanguage(new Locale("vi", "VN"));
                }
                else {
                    Toast.makeText(MainActivity.this, "Google voice không khả dụng!", Toast.LENGTH_LONG).show();
                    onRestart();
                }
            }
        });

        tvReport = (TextView) findViewById(R.id.tvReport);

        cameraPreview = (LinearLayout) findViewById(R.id.camera_preview);
        mPreview = new CameraPreview(myContext, mCamera);
        cameraPreview.addView(mPreview);

        start = (Button) findViewById(R.id.button_start);
        start.setOnClickListener(startListener);

        capture = (Button) findViewById(R.id.button_capture);
        capture.setOnClickListener(captureListener);
    }


//=============================================================================//ham xu li su kien


    View.OnClickListener startListener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            if (MY_PARAMETER_CONTROL == 1)
                return;
            capture.setEnabled(false);
            start.setEnabled(false);
            CHECK_TEST_CAMERA_INTERNAL = 0;
            MY_PARAMETER_CONTROL = 1;
            if (CHECK_CAMERA_TYPE == 0){
//                while (true) {
//                    capture();
//                    // gui anh bitmap x * 418 va 418 * y qua server
//                    // nhan thong bao tu server
//                    String report = null;
//                    speakWords(report);
//                }
//            else {
//                while (true) {
//                    captureRel();
//                    // gui anh bitmap 418 * 418 qua server
//                    // nhan thong bao tu server
//                    String report = null;
//                    speakWords(report);
//                }
            }

        }
    };

    OnClickListener captureListener = new OnClickListener() {
        @Override
        public void onClick(View v) {
            //set camera to continually auto-focus
            mCamera.takePicture(null, null, mPicture);
            mPicture = getPictureCallback();
        }
    };

    private void capture() {
        //set camera to continually auto-focus
        mCamera.takePicture(null, null, mPicture);
        mPicture = getPictureCallback();
    }

    private void captureRel(){

    }

    private void speakWords(String speech) {

        //speak straight away
        myTTS.speak(speech, TextToSpeech.QUEUE_FLUSH, null);
    }
    private void speakWords(TextView textView) {
        String text = textView.getText().toString();
        //speak straight away
        myTTS.speak(text, TextToSpeech.QUEUE_FLUSH, null);
    }


//=============================================================================//ham ho tro camera


    private boolean hasCamera(Context context) {
        //check if the device has camera
        if (context.getPackageManager().hasSystemFeature(PackageManager.FEATURE_CAMERA)) {
            return true;
        } else {
            return false;
        }
    }

    private PictureCallback getPictureCallback() {
        PictureCallback picture = new PictureCallback() {

            @Override
            public void onPictureTaken(byte[] data, Camera camera) {
                //make a new picture file
                String string_toast_report = "";

                if (CHECK_TEST_CAMERA_INTERNAL == 1) {
                    File pictureFile = getOutputMediaFile();

                    if (pictureFile == null) {
                        Toast toast = Toast.makeText(myContext, "Picture not saved and ", Toast.LENGTH_LONG);
                        toast.show();
                        return;
                    }
                    try {
                        //write the file
                        FileOutputStream fos = new FileOutputStream(pictureFile);
                        fos.write(data);
                        fos.close();
                        string_toast_report = string_toast_report + "Picture saved and ";

                    } catch (FileNotFoundException e) {
                    } catch (IOException e) {
                    }
                }

                Bitmap bitmap = BitmapFactory.decodeByteArray(data, 0, data.length);
                if (bitmap == null) {
                    Toast.makeText(MainActivity.this, "Captured image is empty", Toast.LENGTH_LONG).show();
                    return;
                }

// Gui xu li 2 bitmap duoi den server
                bitmap_x418 = Bitmap.createScaledBitmap(bitmap, bitmap.getWidth(), 418, true);
                bitmap_418y = Bitmap.createScaledBitmap(bitmap, 418, bitmap.getHeight(), true);

                string_toast_report = string_toast_report + " processing";
                Toast.makeText(myContext, string_toast_report, Toast.LENGTH_LONG).show();

                //refresh camera to continue preview
                mPreview.refreshCamera(mCamera);
            }
        };
        return picture;
    }

    private File getOutputMediaFile() {
        File mediaStorageDir = new File(Environment.getExternalStoragePublicDirectory(
                Environment.DIRECTORY_PICTURES), "BKSEEING");

        if (!mediaStorageDir.exists()) {
            if (!mediaStorageDir.mkdirs()) {
                Log.d("CameraDemo", "failed to create directory");
                Toast.makeText(myContext, "Failed to create dicectory", Toast.LENGTH_LONG).show();
                return null;
            }
        }

        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        return new File(mediaStorageDir.getPath() + File.separator +
                "IMG_" + timeStamp + ".jpg");
    }

    private void releaseCamera() {
        // stop and release camera
        if (mCamera != null) {
            mCamera.release();
            mCamera = null;
        }
    }


//=============================================================================//



}

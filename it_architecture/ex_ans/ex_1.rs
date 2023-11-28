// トレイトの定義
trait Sensor<T> {
    fn read(&self) -> T;
}

// LightSensor構造体の定義
struct LightSensor {
    value: i32,
}

// LightSensorにSensor<i32>トレイトを実装
impl Sensor<i32> for LightSensor {
    fn read(&self) -> i32 {
        self.value
    }
}

// TemperatureSensor構造体の定義
struct TemperatureSensor {
    value: f32,
}

// TemperatureSensorにSensor<f32>トレイトを実装
impl Sensor<f32> for TemperatureSensor {
    fn read(&self) -> f32 {
        self.value
    }
}

// ジェネリック関数addの定義
fn add<T1, T2>(sensor1: &T1, sensor2: &T2) -> i32
where
    T1: Sensor<i32>,
    T2: Sensor<f32>,
{
    sensor1.read() + sensor2.read() as i32
}

fn main() {
    // LightSensorのインスタンス作成
    let light_sensor = LightSensor { value: 42 };

    // TemperatureSensorのインスタンス作成
    let temperature_sensor = TemperatureSensor { value: 23.5 };

    // add関数を使用してLightSensorとTemperatureSensorの値を合計
    let total = add(&light_sensor, &temperature_sensor);

    // 結果を表示
    println!("Total: {}", total);
}

// トレイトの定義
trait Sensor<T> {
    fn read(&self) -> T;
}

// LightSensor構造体の定義
struct LightSensor<T> {
    value: T,
}

// TemperatureSensor構造体の定義
struct TemperatureSensor<T> {
    value: T,
}

// LightSensorにSensorトレイトを実装
impl<T> Sensor<T> for LightSensor<T>
where
    T: Clone,
{
    fn read(&self) -> T {
        self.value.clone()
    }
}

// TemperatureSensorにSensorトレイトを実装
impl<T> Sensor<T> for TemperatureSensor<T>
where
    T: Clone,
{
    fn read(&self) -> T {
        self.value.clone()
    }
}

// ジェネリック関数addの定義
fn add<T>(sensor1: &impl Sensor<T>, sensor2: &impl Sensor<T>) -> T
where
    T: std::ops::Add<Output = T> + Clone,
{
    sensor1.read() + sensor2.read()
}

fn main() {
    // LightSensorのインスタンス作成
    let light_sensor = LightSensor { value: 42 };

    // TemperatureSensorのインスタンス作成
    let temperature_sensor = TemperatureSensor { value: 23 };

    // add関数を使用してLightSensorとTemperatureSensorの値を合計
    let total = add(&light_sensor, &temperature_sensor);

    // 結果を表示
    println!("Total: {:?}", total);
}

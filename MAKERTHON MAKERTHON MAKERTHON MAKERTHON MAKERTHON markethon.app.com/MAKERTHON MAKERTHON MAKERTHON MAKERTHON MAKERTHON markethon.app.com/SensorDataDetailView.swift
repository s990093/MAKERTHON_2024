import SwiftUI

struct SensorDataDetailView: View {
    let sensor: SensorData  // 傳感器數據
    
    var body: some View {
        HStack {  // 橫向排列
            VStack(alignment: .leading, spacing: 30) {  // 元素之間增加一些間隔
                // 電力數據
                VStack {
                    Text("電力:")
                        .font(.headline)  // 粗體標題
                    Text("\(sensor.electricity, specifier: "%.2f") kWh")  // 電力數值，保留兩位小數
                        .font(.body)  // 正文字體
                }
                .padding()  // 卡片內部的間隔
                .background(Color.white)  // 卡片的背景
                .cornerRadius(12)  // 圓角
                .shadow(radius: 4)  // 軟陰影
                
                // 濕度數據
                VStack {
                    Text("濕度:")
                        .font(.headline)  // 粗體標題
                    Text("\(sensor.humidity, specifier: "%.2f")%")  // 濕度數值，保留兩位小數
                        .font(.body)  // 正文字體
                }
                .padding()  // 卡片內部的間隔
                .background(Color.white)  // 卡片的背景
                .cornerRadius(12)  // 圓角
                .shadow(radius: 4)  // 軟陰影
                
                // 額外傳感器信息
                VStack {
                    Text("裝置 ID:")
                        .font(.headline)  // 粗體標題
                    Text("\(sensor.device_id)")  // 裝置 ID
                        .font(.body)  // 正文字體
                }
                .padding()  // 卡片內部的間隔
                .background(Color.white)  // 卡片的背景
                .cornerRadius(12)  // 圓角
                .shadow(radius: 4)  // 軟陰影
            }
            .padding()  // 總體間隔

            Spacer()  // 在左邊和右邊之間增加間距
            
            // 圖像部分
            Image("img")  // 圖像名稱
                .resizable()  // 使圖像可調整大小
                .aspectRatio(contentMode: .fit)  // 保持比例
                .frame(width: 300, height: 300)  // 固定大小
                .padding()  // 圖像的內部間隔
        }
        .padding()  // 外部間隔
        .background(Color.gray.opacity(0.1))  // 輕微灰色背景
    }
}

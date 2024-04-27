import SwiftUI

struct RescueView: View {
    @State private var offsetY: CGFloat = 0
    private let triggerThreshold: CGFloat = 400
    @State private var isTriggered = false
    @State private var showAlert = false
    
    var body: some View {
        VStack {
            Text("拉下拉桿警急求助")
                .font(.system(size: 40))
                .padding()
            
            Spacer()
            
            ZStack {
                // 背景區域，展示觸發門檻
                Rectangle()
                    .frame(width: 150, height: 500)
                    .foregroundColor(Color.gray.opacity(0.2))
                    .cornerRadius(25)
                    .overlay(
                        Rectangle() // 拉桿的可視效果
                            .frame(width: 150, height: max(0, offsetY))
                            .foregroundColor(.green) // 觸發後的顏色
                            .cornerRadius(25)
                            .animation(.linear, value: offsetY) // 動畫效果
                    )
                
                // 拉桿
                Rectangle()
                    .frame(width: 150, height: 75)
                    .foregroundColor(.blue)
                    .cornerRadius(15)
                    .shadow(radius: 10)
                    .overlay(Text("拉下").font(.title).foregroundColor(.white))
                    .offset(y: offsetY - 200) // 將拉桿置於起點
                    .gesture(
                        DragGesture()
                            .onChanged { value in
                                // 更新偏移量，並將其限制在 0 和觸發門檻之間
                                offsetY = min(max(0, value.translation.height), triggerThreshold)
                            }
                            .onEnded { value in
                                // 如果達到觸發門檻
                                if offsetY >= triggerThreshold {
                                    isTriggered = true
                                    showAlert = true
                                    postToServer(isclick: true) // 發送信號
                                } else {
                                    isTriggered = false
                                    postToServer(isclick: false) // 取消信號
                                }
                                // 重置 offsetY，如果觸發了就保持在門檻處，否則重置為 0
                                offsetY = isTriggered ? triggerThreshold : 0
                            }
                    )
            }
            
            Spacer() // 在拉桿下方留出空間
        }
        .alert(isPresented: $showAlert) {
            Alert(
                title: Text("求助信號已發送"),
                message: Text("已通知相關部門"),
                dismissButton: .default(Text("確定"))
            )
        }
    }
    
    
}

struct RescueView_Previews: PreviewProvider {
    static var previews: some View {
        RescueView()
    }
}

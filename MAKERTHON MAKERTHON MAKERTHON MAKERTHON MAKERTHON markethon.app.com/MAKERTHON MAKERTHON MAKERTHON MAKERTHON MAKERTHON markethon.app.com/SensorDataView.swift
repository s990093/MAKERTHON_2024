import SwiftUI
import Charts

struct SensorDataView: View {
    @ObservedObject var viewModel = SensorDataViewModel()  // Observe the view model
    
    var body: some View {
        
        
        List(viewModel.sensorData, id: \.id) { sensor in  // Correct list usage
            SensorDataDetailView(sensor: sensor)  // Correct passing of non-binding
        }
        .background(Color.gray.opacity(0.9))  // Light gray background for the view

        
        .onAppear {
            viewModel.startTimer()  // Start the timer when the view appears
        }
        
    }
}

//struct SensorDataView_Previews: PreviewProvider {
//    static var previews: SensorDataView {
//        SensorDataView()
//    }
//}

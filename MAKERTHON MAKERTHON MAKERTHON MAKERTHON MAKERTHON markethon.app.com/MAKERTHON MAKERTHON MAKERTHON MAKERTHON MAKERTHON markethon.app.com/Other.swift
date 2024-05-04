//
//  Other.swift
//  MAKERTHON MAKERTHON MAKERTHON MAKERTHON MAKERTHON markethon.app.com
//
//  Created by laihungwei on 2024/5/4.
//

import Foundation

import SwiftUI
import Combine
import Charts  // Include this for using charts in SwiftUI

class SensorDataViewModel: ObservableObject {
    @Published var sensorData: [SensorData] = []  // The sensor data to be displayed
    private var dataService = SensorDataService()  // The data service for fetching sensor data
    private var timer: AnyCancellable?

    init() {
        startTimer()  // Start the timer to fetch data every second
    }

    func startTimer() {
        timer = Timer.publish(every: 1.0, on: .main, in: .common).autoconnect().sink { _ in
            self.fetchSensorData()
        }
    }

    func fetchSensorData() {
        dataService.fetchSensorData { [weak self] result in
            DispatchQueue.main.async {  // Ensure updates are on the main thread
                switch result {
                case .success(let data):
                    // Ensure only 100 data points are retained
                    self?.sensorData = data
                case .failure(let error):
                    print("Error fetching sensor data: \(error)")
                }
            }
        }
    }

    deinit {
        timer?.cancel()  // Cancel the timer when the view model is deallocated
    }
}

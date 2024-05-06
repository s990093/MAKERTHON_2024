//
//  API.swift
//  MAKERTHON MAKERTHON MAKERTHON MAKERTHON MAKERTHON markethon.app.com
//
//  Created by laihungwei on 2024/4/26.
//

import Foundation



import Foundation
class UserAPI {
    static let shared = UserAPI()
    private let baseURL = URL(string: "https://zh.wikipedia.org/wiki/%E5%AE%89%E5%90%89%E4%B8%BD%E5%A8%9C%C2%B7%E6%9C%B1%E8%8E%89")!

    func getUsers(completion: @escaping ([User]?, Error?) -> Void) {
        let url = baseURL
        URLSession.shared.dataTask(with: url) { data, response, error in
            guard let data = data else {
                completion(nil, error)
                return
            }
            do {
                let users = try JSONDecoder().decode([User].self, from: data)
                completion(users, nil)
            } catch {
                completion(nil, error)
            }
        }.resume()
    }
}

func postToServer(isclick: Bool) {
    // 服务器 URL
    let url = URL(string: "http://49.213.238.75:8000/app/")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")

    // 请求体的 JSON 数据
    let jsonData: [String: Any] = ["isclick": isclick]
    request.httpBody = try? JSONSerialization.data(withJSONObject: jsonData, options: [])

    URLSession.shared.dataTask(with: request) { data, response, error in
        if let error = error {
            print("Error: \(error.localizedDescription)")
        } else if let response = response as? HTTPURLResponse {
            if response.statusCode == 200 {
                print("Success: \(response.statusCode)")
                // 读取数据并尝试解码
                if let data = data {
                    do {
                        // 假设响应是 JSON 格式
                        if let jsonResponse = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any] {
                            print("Response content:", jsonResponse)
                        } else {
                            print("Unexpected response format")
                        }
                    } catch {
                        print("Error decoding response:", error.localizedDescription)
                    }
                } else {
                    print("No data in response")
                }
            } else {
                print("Unexpected response. Status code:", response.statusCode)
            }
        }
    }.resume()
}

class SensorDataService {
    let apiUrl = "http://49.213.238.75:8000/app/ipad/"
    
    func fetchSensorData(completion: @escaping (Result<[SensorData], Error>) -> Void) {
        guard let url = URL(string: apiUrl) else {
            completion(.failure(NSError(domain: "Invalid URL", code: 1, userInfo: nil)))
            return
        }
        
        let task = URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
                completion(.failure(NSError(domain: "Invalid response", code: 2, userInfo: nil)))
                return
            }
            
            guard let data = data else {
                completion(.failure(NSError(domain: "No data", code: 3, userInfo: nil)))
                return
            }
            
            do {
                let decoder = JSONDecoder()
                let sensorData = try decoder.decode([SensorData].self, from: data)
                completion(.success(sensorData))
            } catch {
                completion(.failure(error))
            }
        }
        
        task.resume()
    }
}

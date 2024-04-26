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

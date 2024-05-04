//
//  Model.swift
//  MAKERTHON MAKERTHON MAKERTHON MAKERTHON MAKERTHON markethon.app.com
//
//  Created by laihungwei on 2024/4/26.
//

import Foundation

struct User: Codable {
    let id: Int
    let name: String
    let email: String
}

struct SensorData: Codable {
    let id: Int
    let device_id: Int
    let location: String
    let timestamp: String
    let electricity: Double
    let humidity: Double
    let people_count: Int
    let is_sprinkling: Bool
}

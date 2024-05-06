import SwiftUI

struct ContentView: View {
//    @State private var users: [User] = []
    @State private var isLoading = false
    
    var body: some View {
        TabView {
            SensorDataView()
                .tabItem {
                    Image(systemName: "1.circle")
                    Text("資訊")
                }
            
            SecondView()
                .tabItem {
                    Image(systemName: "2.circle")
                    Text("Second")
                }
            
            ThirdView()
                .tabItem {
                    Image(systemName: "3.circle")
                    Text("Third")
                }
        }
//        .onAppear {
//            fetchUsers()
//        }
    }
    
//    func fetchUsers() {
//        isLoading = true
//        UserAPI.shared.getUsers { users, error in
//            DispatchQueue.main.async {
//                isLoading = false
//                if let users = users {
//                    self.users = users
//                } else if let error = error {
//                    // Handle error
//                    print("Failed to fetch users: \(error.localizedDescription)")
//                }
//            }
//        }
//    }
}



struct SecondView: View {
    var body: some View {
        Text("Second View")
            .font(.largeTitle)
    }
}

struct ThirdView: View {
    var body: some View {
        Text("Third View")
            .font(.largeTitle)
    }
}


struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

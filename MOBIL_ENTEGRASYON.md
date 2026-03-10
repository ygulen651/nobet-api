# 📱 Mobil Uygulama Entegrasyonu

## 🚀 API Kurulumu

### 1. Flask Kur

```bash
pip install flask flask-cors
```

### 2. API'yi Başlat

```bash
python api_server.py
```

API şu adreste çalışacak: `http://localhost:5000`

## 📡 API Endpoint'leri

### 1. Tüm Eczaneleri Getir

```
GET http://localhost:5000/api/pharmacies
```

**Örnek Yanıt:**
```json
{
  "success": true,
  "count": 7,
  "cached": "2025-12-15T10:30:00",
  "data": [
    {
      "region": "Merkez Nöbetçi",
      "date": "15-12-2025",
      "name": "BÜYÜK",
      "until": "15/12/2025 23:59'e kadar",
      "phone": "0338 213 28 28",
      "address": "Tahsin Ünal Mah. Kuğulu Park Karşısı 26. SK. NO: 4/A",
      "map": "https://maps.google.com/?ll=37.182773,33.215521..."
    }
  ]
}
```

### 2. Bölgeye Göre Filtrele

```
GET http://localhost:5000/api/pharmacies/merkez
GET http://localhost:5000/api/pharmacies/ermenek
```

### 3. Cache'i Yenile

```
POST http://localhost:5000/api/refresh
```

## 📱 Mobil Uygulama Örnekleri

### Android (Kotlin/Java)

#### Retrofit Kullanarak

```kotlin
// ApiService.kt
interface PharmacyApiService {
    @GET("api/pharmacies")
    suspend fun getAllPharmacies(): PharmacyResponse
    
    @GET("api/pharmacies/{region}")
    suspend fun getPharmaciesByRegion(
        @Path("region") region: String
    ): PharmacyResponse
}

// Data Classes
data class PharmacyResponse(
    val success: Boolean,
    val count: Int,
    val data: List<Pharmacy>
)

data class Pharmacy(
    val region: String,
    val date: String,
    val name: String,
    val until: String?,
    val phone: String?,
    val address: String?,
    val map: String?
)

// ViewModel
class PharmacyViewModel : ViewModel() {
    private val _pharmacies = MutableStateFlow<List<Pharmacy>>(emptyList())
    val pharmacies: StateFlow<List<Pharmacy>> = _pharmacies
    
    fun fetchPharmacies() {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.api.getAllPharmacies()
                if (response.success) {
                    _pharmacies.value = response.data
                }
            } catch (e: Exception) {
                Log.e("PharmacyVM", "Error: ${e.message}")
            }
        }
    }
}
```

#### OkHttp Kullanarak (Basit)

```kotlin
fun fetchPharmacies() {
    val client = OkHttpClient()
    val request = Request.Builder()
        .url("http://YOUR_SERVER_IP:5000/api/pharmacies")
        .build()
    
    client.newCall(request).enqueue(object : Callback {
        override fun onResponse(call: Call, response: Response) {
            val jsonData = response.body?.string()
            val pharmacies = parseJson(jsonData)
            // UI'yi güncelle
        }
        
        override fun onFailure(call: Call, e: IOException) {
            Log.e("API", "Hata: ${e.message}")
        }
    })
}
```

### iOS (Swift)

```swift
// Pharmacy.swift
struct PharmacyResponse: Codable {
    let success: Bool
    let count: Int
    let data: [Pharmacy]
}

struct Pharmacy: Codable {
    let region: String
    let date: String
    let name: String
    let until: String?
    let phone: String?
    let address: String?
    let map: String?
}

// PharmacyService.swift
class PharmacyService {
    func fetchPharmacies(completion: @escaping ([Pharmacy]?) -> Void) {
        guard let url = URL(string: "http://YOUR_SERVER_IP:5000/api/pharmacies") else {
            completion(nil)
            return
        }
        
        URLSession.shared.dataTask(with: url) { data, response, error in
            guard let data = data, error == nil else {
                completion(nil)
                return
            }
            
            do {
                let response = try JSONDecoder().decode(PharmacyResponse.self, from: data)
                completion(response.data)
            } catch {
                print("Parse error: \(error)")
                completion(nil)
            }
        }.resume()
    }
}

// ViewModel (SwiftUI)
class PharmacyViewModel: ObservableObject {
    @Published var pharmacies: [Pharmacy] = []
    private let service = PharmacyService()
    
    func loadPharmacies() {
        service.fetchPharmacies { [weak self] pharmacies in
            DispatchQueue.main.async {
                self?.pharmacies = pharmacies ?? []
            }
        }
    }
}
```

### React Native (JavaScript/TypeScript)

```javascript
// PharmacyService.js
const API_BASE_URL = 'http://YOUR_SERVER_IP:5000';

export const fetchPharmacies = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/pharmacies`);
    const data = await response.json();
    
    if (data.success) {
      return data.data;
    }
    return [];
  } catch (error) {
    console.error('API Error:', error);
    return [];
  }
};

export const fetchPharmaciesByRegion = async (region) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/pharmacies/${region}`);
    const data = await response.json();
    return data.data;
  } catch (error) {
    console.error('API Error:', error);
    return [];
  }
};

// PharmacyScreen.js
import React, { useEffect, useState } from 'react';
import { View, Text, FlatList } from 'react-native';
import { fetchPharmacies } from './PharmacyService';

const PharmacyScreen = () => {
  const [pharmacies, setPharmacies] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    loadPharmacies();
  }, []);
  
  const loadPharmacies = async () => {
    setLoading(true);
    const data = await fetchPharmacies();
    setPharmacies(data);
    setLoading(false);
  };
  
  return (
    <View>
      <FlatList
        data={pharmacies}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.pharmacyCard}>
            <Text style={styles.name}>{item.name}</Text>
            <Text>{item.address}</Text>
            <Text>{item.phone}</Text>
            <Text>{item.until}</Text>
          </View>
        )}
      />
    </View>
  );
};
```

### Flutter (Dart)

```dart
// pharmacy_model.dart
class PharmacyResponse {
  final bool success;
  final int count;
  final List<Pharmacy> data;
  
  PharmacyResponse({
    required this.success,
    required this.count,
    required this.data,
  });
  
  factory PharmacyResponse.fromJson(Map<String, dynamic> json) {
    return PharmacyResponse(
      success: json['success'],
      count: json['count'],
      data: (json['data'] as List)
          .map((e) => Pharmacy.fromJson(e))
          .toList(),
    );
  }
}

class Pharmacy {
  final String region;
  final String date;
  final String name;
  final String? until;
  final String? phone;
  final String? address;
  final String? map;
  
  Pharmacy({
    required this.region,
    required this.date,
    required this.name,
    this.until,
    this.phone,
    this.address,
    this.map,
  });
  
  factory Pharmacy.fromJson(Map<String, dynamic> json) {
    return Pharmacy(
      region: json['region'],
      date: json['date'],
      name: json['name'],
      until: json['until'],
      phone: json['phone'],
      address: json['address'],
      map: json['map'],
    );
  }
}

// pharmacy_service.dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class PharmacyService {
  static const String baseUrl = 'http://YOUR_SERVER_IP:5000';
  
  Future<List<Pharmacy>> fetchPharmacies() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/pharmacies'),
      );
      
      if (response.statusCode == 200) {
        final jsonData = json.decode(utf8.decode(response.bodyBytes));
        final pharmacyResponse = PharmacyResponse.fromJson(jsonData);
        return pharmacyResponse.data;
      }
      return [];
    } catch (e) {
      print('Error: $e');
      return [];
    }
  }
}

// pharmacy_screen.dart
class PharmacyScreen extends StatefulWidget {
  @override
  _PharmacyScreenState createState() => _PharmacyScreenState();
}

class _PharmacyScreenState extends State<PharmacyScreen> {
  final PharmacyService _service = PharmacyService();
  List<Pharmacy> _pharmacies = [];
  bool _isLoading = true;
  
  @override
  void initState() {
    super.initState();
    _loadPharmacies();
  }
  
  Future<void> _loadPharmacies() async {
    setState(() => _isLoading = true);
    final pharmacies = await _service.fetchPharmacies();
    setState(() {
      _pharmacies = pharmacies;
      _isLoading = false;
    });
  }
  
  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Center(child: CircularProgressIndicator());
    }
    
    return ListView.builder(
      itemCount: _pharmacies.length,
      itemBuilder: (context, index) {
        final pharmacy = _pharmacies[index];
        return Card(
          child: ListTile(
            title: Text(pharmacy.name),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(pharmacy.address ?? ''),
                Text(pharmacy.phone ?? ''),
                Text(pharmacy.until ?? ''),
              ],
            ),
          ),
        );
      },
    );
  }
}
```

## 🌐 Sunucu Deployment

### Ücretsiz Hosting Seçenekleri

#### 1. Render.com (Önerilen)
- Ücretsiz plan mevcut
- Otomatik SSL
- GitHub entegrasyonu

#### 2. PythonAnywhere
- Ücretsiz plan
- Kolay setup

#### 3. Heroku (Ücretli)
- Güvenilir
- Kolay deploy

### Render.com ile Deploy

1. `render.yaml` oluştur:

```yaml
services:
  - type: web
    name: nobet-eczane-api
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn api_server:app"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

2. `requirements.txt`'e ekle:
```
gunicorn==21.2.0
```

3. GitHub'a push et ve Render'da bağla

## 🔒 Güvenlik

### API Key Ekle (Opsiyonel)

```python
# api_server.py içine ekle
API_KEY = "your-secret-key"

@app.before_request
def check_api_key():
    if request.endpoint not in ['home']:
        key = request.headers.get('X-API-Key')
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
```

Mobil uygulamadan:
```kotlin
val request = Request.Builder()
    .url(url)
    .addHeader("X-API-Key", "your-secret-key")
    .build()
```

## 📊 Cache Stratejisi

API otomatik olarak 5 dakika cache kullanır. Bu:
- Sunucu yükünü azaltır
- Karaman Eczacı Odası sitesine fazla istek atmaz
- Hızlı yanıt süresi sağlar

Manuel yenileme için `/api/refresh` endpoint'ini kullan.

## ⚡ Test Et

```bash
# Terminal'den test
curl http://localhost:5000/api/pharmacies

# veya Postman/Insomnia kullan
```

## 🎯 Özet

1. ✅ `api_server.py` çalıştır
2. ✅ Mobil uygulamandan HTTP isteği yap
3. ✅ JSON verisini parse et ve göster
4. ✅ Production'da sunucuya deploy et


class GasData {
  final String gasCount;
  final List<dynamic> gasBeanList;

  GasData({required this.gasCount, required this.gasBeanList});

  factory GasData.fromJson(Map<String, dynamic> json) {
    return GasData(
        gasCount: json['gasCount'], gasBeanList: json['gasBeanList']);
  }
}

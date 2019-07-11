// pages/recommedation/recommedation.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    result: app.globalData.result
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    //把结果转为文本形式
    var results = app.globalData.result
    var res = ''
    for (var k in results) {
      res += k + '\n' + results[k] + '\n\n'
    }
    this.setData({result : res})
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})
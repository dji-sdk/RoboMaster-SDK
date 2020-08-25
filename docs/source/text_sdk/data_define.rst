========
数据说明
========

.. data:: switch_enum

    - ``on`` : 打开
    - ``off`` : 关闭


.. data:: mode_enum

    - ``chassis_lead`` : 云台跟随底盘模式
    - ``gimbal_lead`` : 底盘跟随云台模式
    - ``free`` : 自由模式

.. data:: chassis_push_attr_enum

    - ``position`` : 底盘位置
    - ``attitude`` : 底盘姿态
    - ``status`` : 底盘状态

.. data:: gimbal_push_attr_enum

    - ``attitude`` 云台姿态

.. data:: armor_event_attr_enum

    - ``hit`` : 装甲被敲击

.. data:: sound_event_attr_enum

    - ``applause`` : 掌声

.. data:: led_comp_enum

    - ``all`` : 所有 LED 灯
    - ``top_all`` : 云台所有 LED 灯
    - ``top_right`` : 云台右侧 LED 灯
    - ``top_left`` : 云台左侧 LED 灯

    - ``bottom_all`` : 底盘所有 LED 灯
    - ``bottom_front`` : 底盘前侧 LED 灯
    - ``bottom_back`` : 所有后侧 LED 灯
    - ``bottom_left`` : 所有左侧 LED 灯
    - ``bottom_right`` : 所有右侧 LED 灯

.. data:: led_effect_enum

    - ``solid`` : 常亮效果
    - ``off`` : 熄灭效果
    - ``pulse`` : 呼吸效果
    - ``blink`` : 闪烁效果
    - ``scrolling`` : 跑马灯

.. data:: line_color_enum

    - ``red`` : 红色
    - ``blue`` : 蓝色
    - ``green`` : 绿色

.. data:: marker_color_enum

    - ``red`` : 红色
    - ``blue`` : 蓝色

.. data:: ai_push_attr_enum

    - ``person`` : 行人
    - ``gesture`` : 姿势
    - ``line`` ：线
    - ``marker`` : 视觉标签
    - ``robot`` : 机器人

.. data:: ai_pose_id_enum

    - ``4`` : 正V手势
    - ``5`` : 倒V手势
    - ``6`` : 拍照手势

.. data:: ai_marker_id_enum

    - ``1`` : 停止
    - ``4`` : 左转
    - ``5`` : 右转
    - ``6`` : 前进
    - ``8`` : 红心
    - ``10 - 19`` : 数字 0 - 9
    - ``20 - 45`` : 字母 A - Z

.. data:: camera_ev_enum

    - ``default`` : 默认值
    - ``small`` : 小
    - ``medium`` : 中
    - ``large`` : 大

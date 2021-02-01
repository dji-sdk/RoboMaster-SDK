========
數據說明
========

.. data:: switch_enum

    - ``on`` : 打開
    - ``off`` : 關閉


.. data:: mode_enum

    - ``chassis_lead`` : 雲台跟隨底盤模式
    - ``gimbal_lead`` : 底盤跟隨雲台模式
    - ``free`` : 自由模式

.. data:: chassis_push_attr_enum

    - ``position`` : 底盤位置
    - ``attitude`` : 底盤姿態
    - ``status`` : 底盤狀態

.. data:: gimbal_push_attr_enum

    - ``attitude`` 雲台姿態

.. data:: armor_event_attr_enum

    - ``hit`` : 裝甲被敲擊

.. data:: sound_event_attr_enum

    - ``applause`` : 掌聲

.. data:: led_comp_enum

    - ``all`` : 所有 LED 燈
    - ``top_all`` : 雲台所有 LED 燈
    - ``top_right`` : 雲台右側 LED 燈
    - ``top_left`` : 雲台左側 LED 燈

    - ``bottom_all`` : 底盤所有 LED 燈
    - ``bottom_front`` : 底盤前側 LED 燈
    - ``bottom_back`` : 所有後側 LED 燈
    - ``bottom_left`` : 所有左側 LED 燈
    - ``bottom_right`` : 所有右側 LED 燈

.. data:: led_effect_enum

    - ``solid`` : 常亮效果
    - ``off`` : 熄滅效果
    - ``pulse`` : 呼吸效果
    - ``blink`` : 閃爍效果
    - ``scrolling`` : 跑馬燈

.. data:: line_color_enum

    - ``red`` : 紅色
    - ``blue`` : 藍色
    - ``green`` : 綠色

.. data:: marker_color_enum

    - ``red`` : 紅色
    - ``blue`` : 藍色

.. data:: ai_push_attr_enum

    - ``person`` : 行人
    - ``gesture`` : 姿勢
    - ``line`` ：線
    - ``marker`` : 視覺標籤
    - ``robot`` : 機器人

.. data:: ai_pose_id_enum

    - ``4`` : 正V手勢
    - ``5`` : 倒V手勢
    - ``6`` : 拍照手勢

.. data:: ai_marker_id_enum

    - ``1`` : 停止
    - ``4`` : 左轉
    - ``5`` : 右轉
    - ``6`` : 前進
    - ``8`` : 紅心
    - ``10 - 19`` : 數字 0 - 9
    - ``20 - 45`` : 字母 A - Z

.. data:: camera_ev_enum

    - ``default`` : 默認值
    - ``small`` : 小
    - ``medium`` : 中
    - ``large`` : 大

## 一.对象的创建与销毁
### 1.用静态工厂方法代替构造器
###### 优点
* 1.有名称
* 2.不必在每次调用的时候都创建一个新对象：静态工厂方法能够为重复的调用返回相同的对象
* 3.可以返回原返回类型的任何子类型的对象
* 4.所返回对象的类可以随着每次调用而发生变化，这取决于静态工厂方法的参数值
* 5.方法返回对象所属的类，在编写包含该静态工厂方法的类时可以不存在。
###### 缺点：
* 1.类如果不包含共有的或者受保护的构造器，就不能被子类化
* 2.程序员很难发现他们;
### 2.遇到多个构造器参数时要考虑使用构建器
* 重叠构造器
* Java Bean
* Builder 建造者模式
### 3.用私有构造器或者枚举类型强化Singleton属性
实现Singleton有两种方法：
两种方法都要保持构造器为私有的，并导出共有的静态成员，以便允许客户端能够访问该类的唯一类型
* 1：

### 4.通过私有构造器强化不可实例化的能力
### 5.优先考虑依赖注入来引入资源

### 6.避免创建不必要的对象
### 7.消除过期的对象引用
### 8.避免使用终结方法和清楚方法
* 永远不应该依赖终结方法和清除方法来更新重要的持久状态
* 使用终结方法和清除方法有重要的性能损失
* 除非是作为安全网，或者是为了终止非关键的本地资源，不要使用清除方法
### 9.try-with-resources优先于try-finally

## 二.对所有对象都通用的方法

### 10.覆盖equals时请遵守通用约定
 * 自反性，对称性，传递性，一致性，非空性
 * 不要将equals声明中的Object对象替换为其他的类型
### 11.覆盖equals时总要覆盖hashcode
* 原因： 会违反hashcode的通用约定，导致该类无法结合所有基于散列的集合一起正常运作；HashSet，HashMap；
* 相等的对象必须具有相等的散列码（hashcode）
### 12.始终要覆盖toString方法
### 13.谨慎的覆盖clone
### 14.考虑实现Comparable接口

## 三.类和接口

### 15.使类和成员的可访问性最小
* 公有类的实例域绝不能是公有的；
* 包含公有可变域的类通常不是线程安全的；
### 16.要在公有类而非公有域中使用访问方法
### 17.使可变性最小化
* 使类不可变需要遵循的原则
  
  1. 不要提供任何会修改对象状态的方法
  2. 保证类不会被扩展
  3. 声明所有域都是final的
  4. 声明所有域都是私有的
  5. 确保对于任何可变组件的互斥访问
### 18.复合优先于继承
### 19.要么设计继承并提供说明文档，要么禁止继承
### 20.接口优先于抽象类
### 21.为后代设计接口
### 22.接口只用于定义类型
### 23.类层次优先于标签类
### 24.静态成员类优先于非静态成员类
### 25.限制源文件为单个顶级类
 
## 四.泛型
### 26.请不要使用原生态类型
### 27.消除非受检的警告
### 28.列表优于数组
### 29.优先考虑泛型
### 30.优先考虑泛型方法
### 31.利用有限制通配符来提高API的灵活性
### 32.谨慎并用泛型和可变参数
### 33.优先考虑类型安全的异构容器
## 六.枚举和注解
### 34.用enum代替int常量
### 35.用实例域代替序数
### 36.用EnumSet代替位域
### 37.用EnumMap代替序数索引
### 38.用接口模拟可扩展的枚举
### 39.注解优先于命名模式
### 40.坚持使用Override注解
### 41.用标记接口定义类型
## 七.Lambda和Stream
### 42.Lambda优先于匿名类
### 43.方法引用优先于Lambda
### 44.坚持使用标准的函数接口
### 45.谨慎使用Stream
### 46.优先使用Stream中无副作用的函数
### 47.Stream要优先使用Collection作为返回类型
### 48.谨慎使用Stream并行
## 八.方法

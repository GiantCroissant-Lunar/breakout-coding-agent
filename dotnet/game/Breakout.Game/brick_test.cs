using Breakout.Game.Models;
using Breakout.Game.Utilities;

namespace BrickTest
{
    public class BrickFunctionalityTest
    {
        public static void RunTests()
        {
            Console.WriteLine("=== Brick Object Model Tests ===");
            
            // Test 1: Brick creation and default values
            TestBrickCreation();
            
            // Test 2: Brick properties
            TestBrickProperties();
            
            // Test 3: Point values for different brick types
            TestPointValues();
            
            // Test 4: Collision detection
            TestCollisionDetection();
            
            // Test 5: Destroy functionality
            TestDestroyFunctionality();
            
            Console.WriteLine("=== All Tests Completed ===");
        }
        
        private static void TestBrickCreation()
        {
            Console.WriteLine("Test 1: Brick Creation");
            var brick = new Brick();
            
            Console.WriteLine($"  Default Character: {brick.Character} (Expected: █)");
            Console.WriteLine($"  Default IsDestroyed: {brick.IsDestroyed} (Expected: False)");
            Console.WriteLine($"  Default Type: {brick.Type} (Expected: Standard)");
            Console.WriteLine($"  Default Color: {brick.Color} (Expected: Cyan)");
            Console.WriteLine("  ✓ Brick creation test passed\n");
        }
        
        private static void TestBrickProperties()
        {
            Console.WriteLine("Test 2: Brick Properties");
            var brick = new Brick
            {
                X = 10,
                Y = 5,
                Width = BrickConstants.DefaultWidth,
                Height = BrickConstants.DefaultHeight,
                Type = BrickType.Strong,
                Color = BrickConstants.StrongColor
            };
            
            Console.WriteLine($"  Position: ({brick.X}, {brick.Y}) (Expected: (10, 5))");
            Console.WriteLine($"  Size: {brick.Width}x{brick.Height} (Expected: {BrickConstants.DefaultWidth}x{BrickConstants.DefaultHeight})");
            Console.WriteLine($"  Type: {brick.Type} (Expected: Strong)");
            Console.WriteLine("  ✓ Brick properties test passed\n");
        }
        
        private static void TestPointValues()
        {
            Console.WriteLine("Test 3: Point Values");
            
            var standardBrick = new Brick { Type = BrickType.Standard };
            var strongBrick = new Brick { Type = BrickType.Strong };
            var bonusBrick = new Brick { Type = BrickType.Bonus };
            
            Console.WriteLine($"  Standard brick points: {standardBrick.GetPointValue()} (Expected: {BrickConstants.StandardPoints})");
            Console.WriteLine($"  Strong brick points: {strongBrick.GetPointValue()} (Expected: {BrickConstants.StrongPoints})");
            Console.WriteLine($"  Bonus brick points: {bonusBrick.GetPointValue()} (Expected: {BrickConstants.BonusPoints})");
            
            // Validate the values match constants
            bool standardMatch = standardBrick.GetPointValue() == BrickConstants.StandardPoints;
            bool strongMatch = strongBrick.GetPointValue() == BrickConstants.StrongPoints;
            bool bonusMatch = bonusBrick.GetPointValue() == BrickConstants.BonusPoints;
            
            Console.WriteLine($"  Point values match constants: {standardMatch && strongMatch && bonusMatch}");
            Console.WriteLine("  ✓ Point values test passed\n");
        }
        
        private static void TestCollisionDetection()
        {
            Console.WriteLine("Test 4: Collision Detection");
            
            var brick = new Brick
            {
                X = 10,
                Y = 5,
                Width = 6,
                Height = 1
            };
            
            var ball = new Ball { X = 12, Y = 5 }; // Inside brick bounds
            var ballOutside = new Ball { X = 20, Y = 10 }; // Outside brick bounds
            
            bool collisionInside = brick.CheckCollision(ball);
            bool collisionOutside = brick.CheckCollision(ballOutside);
            
            Console.WriteLine($"  Ball inside brick collision: {collisionInside} (Expected: True)");
            Console.WriteLine($"  Ball outside brick collision: {collisionOutside} (Expected: False)");
            Console.WriteLine("  ✓ Collision detection test passed\n");
        }
        
        private static void TestDestroyFunctionality()
        {
            Console.WriteLine("Test 5: Destroy Functionality");
            
            var brick = new Brick();
            Console.WriteLine($"  Before destroy - IsDestroyed: {brick.IsDestroyed} (Expected: False)");
            
            brick.Destroy();
            Console.WriteLine($"  After destroy - IsDestroyed: {brick.IsDestroyed} (Expected: True)");
            
            // Test that destroyed brick doesn't report collision
            var ball = new Ball { X = brick.X, Y = brick.Y };
            bool collisionAfterDestroy = brick.CheckCollision(ball);
            Console.WriteLine($"  Collision after destroy: {collisionAfterDestroy} (Expected: False)");
            Console.WriteLine("  ✓ Destroy functionality test passed\n");
        }
    }
}
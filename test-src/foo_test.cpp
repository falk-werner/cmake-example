#include "foo.hpp"
#include <gtest/gtest.h>

TEST(foo, incr) 
{
    ASSERT_EQ(1, foo::incr(0));
    ASSERT_EQ(42, foo::incr(41));
}

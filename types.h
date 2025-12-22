#pragma once

#include <cstdint>
#include <bit>
#include <limits>
#include <climits>

using i8 = int8_t;
using i16 = int16_t;
using i32 = int32_t;
using i64 = int64_t;

using ui8 = uint8_t;
using ui16 = uint16_t;
using ui32 = uint32_t;
using ui64 = uint64_t;

using f32 = float;
using f64 = double;

using b8 = bool;

using isize = std::ptrdiff_t;
using usize = std::size_t;

static_assert(std::numeric_limits<f32>::is_iec559, "f32 is not IEEE 754 compliant");
static_assert(std::numeric_limits<f64>::is_iec559, "f64 is not IEEE 754 compliant");
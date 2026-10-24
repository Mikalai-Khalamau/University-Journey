def calculate_area(shape, params)
  if ["circle", "rectangle"].include?(shape) && params
    case shape
    when "circle"
      radius = params.fetch("radius", 0)
      if radius > 0
        return Math::PI * radius ** 2
      end
    when "rectangle"
      width = params.fetch("width", 0)
      height = params.fetch("height", 0)
      if width > 0 && height > 0
        return width * height
      end
    end
  end
  return 0
end

def process_number(item)
  if item > 0
    if item % 2 == 0
      return item ** 2
    else
      return item ** 3
    end
  else
    return 0
  end
end

def process_string(item)
  if item.length > 5
    return item.upcase
  else
    return item.downcase
  end
end

def process_item(item)
  case item
  when Integer
    return process_number(item)
  when String
    return process_string(item)
  else
    return nil
  end
end

def process_data(data)
  data.map { |item| process_item(item) }
end

def main
  shapes = []
  i = 0
  while i < 3
    shape_type = ["circle", "rectangle"].sample
    params = case shape_type
             when "circle"
               { "radius" => rand(-2..5) }
             when "rectangle"
               { "width" => rand(-2..5), "height" => rand(-2..5) }
             end
    area = calculate_area(shape_type, params)
    if area > 0
      shapes.push([shape_type, params, area])
    end
    i += 1
  end

  if shapes.length > 0
    puts "\nValid shapes:"
    for shape in shapes
      puts "#{shape[0]}: #{shape[1]}, Area: #{'%.2f' % shape[2]}"
    end
  end

  test_data = [1, "hello", -5, "world", 0, 8, "abc", -3]
  processed = process_data(test_data)
  puts "\nProcessed data: #{processed.inspect}"
end

main
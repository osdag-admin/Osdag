def calculate_total_width(edge, gauge1, gauge2, cols):
            width = 0
            for i in range(cols - 1):
                if i % 2 == 0:
                    width += gauge1
                else:
                    width += gauge2
            total_width = width + 2 * edge
            return total_width
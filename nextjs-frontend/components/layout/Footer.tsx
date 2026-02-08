export default function Footer() {
  return (
    <footer className="border-t bg-gray-50 dark:bg-gray-900">
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col items-center justify-between gap-4 md:flex-row">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            © 2026 아파트 실거래가 분석 플랫폼. All rights reserved.
          </p>
          <div className="flex gap-4 text-sm text-gray-600 dark:text-gray-400">
            <a
              href="https://www.data.go.kr/"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-gray-900 dark:hover:text-white"
            >
              공공데이터포털
            </a>
            <a
              href="https://www.molit.go.kr/"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-gray-900 dark:hover:text-white"
            >
              국토교통부
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
